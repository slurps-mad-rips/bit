#!/usr/bin/env python

from configparser import ConfigParser
from setuptools import setup

import sys
import os

config = ConfigParser()
config.read(os.path.join(os.getcwd(), 'setup.cfg'))
metadata = config['metadata']
files = config['files']

setup(
    # Config information
    name=metadata['name'],
    version=metadata['version'],
    license=metadata['license'],
    author=metadata['author'],
    url=metadata['home-page'],
    description=metadata['summary'],
    keywords=metadata['keywords'],
    classifiers=metadata['classifiers'].split('\n')[1:],
    install_requires=['distribute'],
    setup_requires=['nose>=1.1.2'],
    test_suite = 'nose.collector',
    # Content/Data
    packages=files['packages'].split('\n')[1:],
    entry_points=dict(console_scripts=['bit=bit:main']),
    # Additional Info
    zip_safe=True
)
