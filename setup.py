#!/usr/bin/env python

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


def symlink_config_files():
    from sysconf.lib import HOMEDIR
    from sysconf.lib import safe_remove
    from sysconf.lib import STATICHOMEDIR
    from sysconf.lib import symlink
    from sysconf.lib import logtitle

    # symlink '.' home files
    logtitle("symlink home config files")
    for name in os.listdir(STATICHOMEDIR):
        src = os.path.join(STATICHOMEDIR, name)
        dst = os.path.join(HOMEDIR, name)
        if name.startswith('.') and os.path.isfile(src):
            safe_remove(dst)
            symlink(src, dst)


def main():
    install_pkg()
    symlink_config_files()



if __name__ == '__main__':
    main()
