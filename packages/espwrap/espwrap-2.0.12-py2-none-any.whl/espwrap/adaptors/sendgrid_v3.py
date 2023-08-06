# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals, absolute_import

import base64
import json
import logging
import sys

import sendgrid
from sendgrid.helpers.mail import (
    Mail, From, To, Cc, Bcc, Subject, Substitution,
    CustomArg, SendAt, Content, MimeType, Attachment, FileName,
    FileContent, ReplyTo, Category, IpPoolName,
    TrackingSettings, ClickTracking,
    OpenTracking, OpenTrackingSubstitutionTag,
    Section)
from python_http_client.exceptions import HTTPError

from espwrap.base import MassEmail, batch, MIMETYPE_HTML, MIMETYPE_TEXT
from espwrap.adaptors.sendgrid_common import breakdown_recipients

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


if sys.version_info > (2,):
    basestring = str


_HTTP_EXC_MSG = 'SendGrid responded with an HTTP-error code.  Email Subject: %s, Status Code: %s, Reason: %s, Body: %s'


class SendGridMassEmail(MassEmail):
    def __init__(self, api_key, *args, **kwargs):
        super(SendGridMassEmail, self).__init__(*args, **kwargs)

        self.client = sendgrid.SendGridAPIClient(api_key)

        self.delimiters = ('-', '-')

    def set_variable_delimiters(self, start='-', end='-'):
        self.delimiters = (start, end)

    def get_variable_delimiters(self, as_dict=False):
        if as_dict:
            return {
                'start': self.delimiters[0],
                'end': self.delimiters[1],
            }
        return self.delimiters

    def add_tags(self, *tags):
        if len(tags) > 10:
            raise Exception('Too many tags, SendGrid limits to 10 per email')

        if len(tags) + len(self.tags) > 10:
            raise Exception('Requested tags would have raised total to above Sendgrid limit of 10')

        return super(SendGridMassEmail, self).add_tags(*tags)

    def message_constructor(self, to_send):
        message = Mail()
        to_emails = []

        # Content (Text)
        if self.body[MIMETYPE_TEXT]:
            content = Content(
                MimeType.text,
                self.body[MIMETYPE_TEXT]
            )
            message.content = content

        # Content (Html)
        if self.body[MIMETYPE_HTML]:
            content = Content(
                MimeType.html,
                self.body[MIMETYPE_HTML]
            )
            message.content = content

        message.subject = Subject(self.subject)

        # Category
        if self.tags:
            for tag in self.tags:
                message.category = Category(tag)

        # Reply
        if self.reply_to_addr:
            message.reply_to = ReplyTo(self.reply_to_addr)

        # Send At
        if self.send_at:
            message.send_at = SendAt(self.send_at)

        # IP Pool
        if self.ip_pool:
            message.ip_pool_name = IpPoolName(self.ip_pool)

        # CC
        if self.cc_list:
            list_cc = [Cc(email) for email in self.cc_list]
            message.cc = list_cc

        # BCC
        if self.bcc_list:
            list_bcc = [Bcc(email) for email in self.cc_list]
            message.bcc = list_bcc

        # Attachment
        if self.attachments:
            for file_name, file_path_or_string in self.attachments.iteritems():
                attachment = Attachment()
                encoded = base64.b64encode(str(file_path_or_string))
                attachment.file_content = FileContent(encoded)
                attachment.file_name = FileName(file_name)
            message.attachment = attachment

        # Webhook Data
        if self.webhook_data:
            for key, val in self.webhook_data.items():
                message.custom_arg = CustomArg(key, val)

        # Metadata
        if self.metadata:
            for key, val in self.metadata.items():
                message.custom_arg = CustomArg(key, val)

        # Template Name
        if self.template_name:
            message.custom_arg = CustomArg('template_name', self.template_name)

        # Tracking
        tracking_settings = TrackingSettings()
        # Opens
        if self.track_opens:
            tracking_settings.open_tracking = OpenTracking(
                self.track_opens,
                OpenTrackingSubstitutionTag("open_tracking")
            )
        # Clicks
        if self.track_clicks:
            tracking_settings.click_tracking = ClickTracking(
                self.track_clicks,
                self.track_clicks
            )
        message.tracking_settings = tracking_settings

        if self.from_addr and self.from_name:
            message.from_email = From(email=self.from_addr, name=self.from_name)
        else:
            message.from_email = From(email=self.from_addr)

        for subgrps in to_send:
            for subgrp in subgrps:
                substitutions = subgrp['merge_vars']
                substitutions_dict = {}

                for key, val in substitutions.items():
                    new_key = '{1}{0}{2}'.format(key, *self.delimiters)
                    formatted_val = val
                    if not isinstance(val, basestring):
                        try:
                            formatted_val = str(val)
                        except UnicodeEncodeError:
                            formatted_val = val.encode('utf-8')

                    substitutions_dict[new_key] = formatted_val

                email = subgrp['email']
                name = subgrp['name']
                to_emails.append(
                    To(
                        email=email,
                        name=name,
                        substitutions=substitutions_dict,
                        subject=self.generate_subject(email, name))
                )

        message.add_to(to_emails, is_multiple=True)

        # Global Subs
        for key, val in self.global_merge_vars.items():
            new_key = '{1}{0}{2}'.format(key, *self.delimiters)
            formatted_val = val
            if not isinstance(val, basestring):
                try:
                    formatted_val = str(val)
                except UnicodeEncodeError:
                    formatted_val = val.encode('utf-8')

            message.substitution = Substitution(new_key, formatted_val)

        return message

    def generate_subject(self, email, name):
        """
        Generate email subject for recipient.
        If username contains "." or "+" it is considered an alias so we
        prepend a custom greeting to avoid bounces from providers like Gmail
        :param email: Recipient email
        :param name: Recipient name
        :return subject: sendgrid.helpers.mail.Subject
        """
        try:
            username = email.split('@')[0]
            if '.' in username or '+' in username:
                return Subject('{} [{}]'.format(self.subject, email))
        except Exception as e:
            logger.exception(e)

        return Subject(self.subject)

    def send(self):

        responses=[]

        self.validate()

        grouped_recipients = batch(list(self.recipients), self.partition)

        for grp in grouped_recipients:
            to_send = breakdown_recipients(grp)

            message = self.message_constructor(to_send)

            # message data as dict for examination/validation below
            message_dict = message.get()

            # do not send if custom args >10 KB (sendgrid rule)
            if 'custom_args' in message_dict:
                message_custom_args = len(json.dumps(message_dict['custom_args']))
                custom_args_size = sys.getsizeof(message_custom_args)
                custom_args_kb = 0.001 * float(custom_args_size)
                if custom_args_kb > 10:
                    raise Exception('attempted to send {} KB custom_args, not to exceed 10 KB.'.format(custom_args_kb))

            # do not send if number of recipients >1000 (sendgrid rule)
            num_recips = len(message_dict['personalizations'])
            if num_recips > 1000:
                raise Exception('attempted to send to {} email addresses, not to exceed 1000 addresses.'.format(num_recips))

            """
            send message and append response from this grp to list of returned responses for all grouped_recipients
            """
            try:
                logger.debug(message)
                response = self.client.send(message)
            except HTTPError as e:
                logger.exception(_HTTP_EXC_MSG, self.subject, e.status_code, e.reason, e.body)
            except Exception:
                logger.exception('Unknown exception while sending a SendGridMassEmail.')
            else:
                responses.append(response)

        # return list of all responses for each grp in grouped_recipients
        return responses
