#!/usr/bin/env python

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
            'sysconf.confsys',
            'sysconf.confuser',
            'sysconf.lib',
        ],
        install_packages=[
            'docopt',
        ]
    )


def confuser():
    for name in os.listdir('sysconf/confuser'):
        if not name.startswith('_') and name.endswith('.py'):
            modname = 'sysconf.confuser.' + os.path.splitext(name)[0]
            mod = importlib.import_module(modname)
            mod.main()


def main():
    install_pkg()
    confuser()



if __name__ == '__main__':
    main()
