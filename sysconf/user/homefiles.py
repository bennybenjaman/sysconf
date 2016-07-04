"""
Copy "." files to user home dir.
"""

import os

from sysconf.lib import DIR_HOME
from sysconf.lib import DIR_STATIC_HOME
from sysconf.lib import safe_remove
from sysconf.lib import sh
from sysconf.lib import symlink
from sysconf.lib import which


def main():
    for name in os.listdir(DIR_STATIC_HOME):
        src = os.path.join(DIR_STATIC_HOME, name)
        dst = os.path.join(DIR_HOME, name)
        if name.startswith('.') and os.path.isfile(src):
            safe_remove(dst)
            symlink(src, dst)

    if which('git'):
        sh("git config --global push.default simple")
