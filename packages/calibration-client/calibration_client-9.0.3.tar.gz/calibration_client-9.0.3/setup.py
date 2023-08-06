#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from os import path

from setuptools import setup, find_packages

# read the contents of your README file
package_dir = path.abspath(path.dirname(__file__))
with open(path.join(package_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def find_version():
    filename = path.join(package_dir, 'calibration_client', '__init__.py')
    with open(filename, 'r', encoding='utf-8') as f:
        vers_file = f.read()
    print('#' * 100)
    print('filename => {0}'.format(filename))
    print('file content => {0}'.format(vers_file.splitlines()[:10]))
    print('#' * 100)
    match = re.search(r"^__version__ = '([.\d]+)'", vers_file, re.M)
    if match is not None:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='calibration_client',
    version=find_version(),
    description='Python Client for European XFEL Calibration Catalogue Web App'
                ' available at https://in.xfel.eu/calibration',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Luís Maia',
    author_email='luis.maia@xfel.eu',
    maintainer='Luís Maia',
    maintainer_email='luis.maia@xfel.eu',
    url='https://git.xfel.eu/gitlab/ITDM/calibration_client',
    platforms='any',
    license='MIT',
    packages=find_packages(),
    install_requires=['oauthlib',
                      'requests',
                      'requests-oauthlib',
                      'oauth2_xfel_client >=6.0',
                      'pytz'],
    extras_require={'test': [
        'pytest',
        'pytest-cov',
        'python-dateutil',
        'pytz',
        'pycodestyle'
    ]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
