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


def install_pkg():
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
        install_packages=[
            'docopt',
        ]
    )


def run_sysinstall():
    from sysconf import sh, logtitle
    logtitle('running sys install')
    sh("./scripts/sysinstall", sudo=True)


def run_sysconfig():
    from sysconf import sh, logtitle
    logtitle('running sys config')
    sh("./scripts/sysconfig", sudo=True)


def run_userconfig():
    from sysconf import sh, logtitle
    logtitle('running user config')
    sh("./scripts/userconfig")


def run_all():
    run_sysinstall()
    run_sysconfig()
    run_userconfig()


def main():
    if sys.argv == ['setup.py', 'develop', '--user']:
        install_pkg()
    else:
        from docopt import docopt
        args = docopt(__doc__)
        if args['sysinstall']:
            run_sysinstall()
        elif args['sysconfig']:
            run_sysconfig()
        elif args['userconfig']:
            run_userconfig()
        elif args['runall']:
            run_all()


if __name__ == '__main__':
    main()
