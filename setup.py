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


def run_scripts_in_dir(path):
    from sysconf.lib import log
    from sysconf.lib import logtitle
    from sysconf.lib import SkipTask

    for name in os.listdir(path):
        if not name.startswith('_') and name.endswith('.py'):
            modname = path.replace('/', '.') + '.' + os.path.splitext(name)[0]
            logtitle("running %s" % modname)
            mod = importlib.import_module(modname)
            try:
                mod.main()
            except SkipTask as exc:
                log("skip", str(exc))


def confuser():
    run_scripts_in_dir('sysconf/confuser')

def confsys():
    run_scripts_in_dir('sysconf/confsys')



def main():
    install_pkg()
    confuser()
    confsys()



if __name__ == '__main__':
    main()
