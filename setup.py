#!/usr/bin/env python

from setuptools import setup

import sys
import os

setup(
    # Config information
    name='bit',
    version='0.4',
    license='BSD',
    author='Tres Walsh',
    url='http://mnmlstc.com',
    description='A minimal build system',
    keywords='bit build-system build-tools minimal small build',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Build Tools',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    install_requires=['distribute'],
    setup_requires=['nose>=1.1.2'],
    test_suite = 'nose.collector',
    # Content/Data
    packages=[
        'bit',
        'bit.core'
    ],
    entry_points=dict(console_scripts=['bit=bit:main']),
    # Additional Info
    zip_safe=True
)
