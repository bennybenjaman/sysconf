#!/usr/bin/env python

"""
Usage:
    make install                             # install all
    setup.py confuser|confsys <subcmd>       # run specific subcmd
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
            'sysconf.confsys',
            'sysconf.confuser',
            'sysconf.lib',
        ],
        install_packages=[
            'docopt',
        ]
    )


def run_script_by_path(path):
    from sysconf.lib import log
    from sysconf.lib import logtitle
    from sysconf.lib import SkipTask

    if path.endswith('.py'):
        path = os.path.splitext(path)[0]
    modname = path.replace('/', '.')
    logtitle("running %s" % modname)
    mod = importlib.import_module(modname)
    try:
        mod.main()
    except SkipTask as exc:
        log("skip", str(exc))


def run_scripts_in_dir(path):
    for name in os.listdir(path):
        if not name.startswith('_') and name.endswith('.py'):
            run_script_by_path(os.path.join(path, name))


def main():
    if sys.argv == ['setup.py', 'develop', '--user']:
        install_pkg()
        run_scripts_in_dir('sysconf/confuser')
        run_scripts_in_dir('sysconf/confsys')
    else:
        # CLI parser
        from sysconf.lib import hilite

        def get_avail_subcmds(subcmd):
            ls = []
            for name in os.listdir('sysconf/' + subcmd):
                if not name.startswith('_') and name.endswith('.py'):
                    ls.append(name)
            return ls


        if len(sys.argv) < 2:
            return sys.exit(__doc__.strip())

        subcmd = sys.argv[1]
        if subcmd not in ('confuser', 'confsys'):
            sys.exit(__doc__.strip())

        # list sub cmds
        if len(sys.argv) == 2:
            subs = get_avail_subcmds(subcmd)
            print("available sub commands:")
            for name in subs:
                print "  " + hilite(os.path.splitext(name)[0], ok=None, bold=1)
        # execute sub cmd
        else:
            run_script_by_path(os.path.join('sysconf', subcmd, sys.argv[2]))




if __name__ == '__main__':
    main()
