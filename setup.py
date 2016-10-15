#!/usr/bin/env python

"""
Personal (Giampaolo) system config utilities to install on a brand new
UNIX system. More at: https://github.com/giampaolo/sysconf

Usage:
    setup sysinstall
    setup sysconfig
    setup userconfig
    setup runall
"""


import os
import sys
from setuptools import setup


HERE = os.path.abspath(os.path.dirname(__file__))
if os.name != 'posix':
    sys.exit('UNIX only')


setup(
    name='sysconf',
    version='0.1',
    description='Personal (Giampaolo) UNIX system utils',
    license='MIT',
    platforms='Platform Independent',
    author="Giampaolo Rodola'",
    author_email='g.rodola@gmail.com',
    py_modules=[
        'sysconf',
    ],
    install_requires=[
        'docopt',
    ]
)
