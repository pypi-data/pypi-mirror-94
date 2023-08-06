from __future__ import print_function, division, unicode_literals

import re
import ast

from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('espwrap/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='espwrap',
    version=version,
    description='A light wrapper around email service providers',
    url='https://github.com/SpotOnInc/espwrap',
    download_url = 'https://github.com/SpotOnInc/espwrap/{0}'.format(version),
    license='MIT',
    author='SpotOn',
    author_email='josh@spoton.com',
    packages=[str('espwrap'), str('espwrap.adaptors')],
    platforms='any',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    extras_require={
        'mandrill': ['mandrill>=1.0.57'],
        'sendgrid': [
            'smtpapi>=0.3.1',
            'sendgrid==6.1.0',
        ],
    }
)
