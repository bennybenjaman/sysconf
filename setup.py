#!/usr/bin/env python

"""
CIao ciao.

Usage:
    setup sysinstall
    setup sysconfig
    setup userconfig
"""


import importlib
import os
import pip  # NOQA
import sys
from setuptools import setup


HERE = os.path.abspath(os.path.dirname(__file__))
if os.name != 'posix':
    sys.exit('UNIX only')


def install_pkg():
    setup(
        name='sysconf',
        version='0.1',
        description='Personal (giampaolo) system utils',
        license='MIT',
        platforms='Platform Independent',
        author="Giampaolo Rodola'",
        author_email='g.rodola@gmail.com',
        packages=[
            'sysconf',
            'sysconf.bin',
            'sysconf.sys',
            'sysconf.user',
            'sysconf.lib',
        ],
        install_packages=[
            'docopt',
        ]
    )


def run_sysinstall():
    from sysconf.lib import sh, logtitle
    logtitle('running sys install')
    sh("./scripts/sysinstall", sudo=True)


def run_sysconfig():
    from sysconf.lib import sh, logtitle
    logtitle('running sys config')
    sh("./scripts/sysconfig", sudo=True)


def run_userconfig():
    from sysconf.lib import sh, logtitle
    logtitle('running user config')
    sh("./scripts/userconfig")


def run_all():
    run_sysinstall()
    run_sysconfig()
    run_userconfig()


def main():
    if sys.argv == ['setup.py', 'develop', '--user']:
        install_pkg()
        run_all()
    else:
        from docopt import docopt
        args = docopt(__doc__)
        if args['sysinstall']:
            run_sysinstall()
        elif args['sysconfig']:
            run_sysconfig()
        elif args['userconfig']:
            run_userconfig()


if __name__ == '__main__':
    main()
