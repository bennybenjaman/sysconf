"""
Copy "." files to user home dir.
"""

import os

from sysconf.lib import DIR_HOME
from sysconf.lib import DIR_STATIC_HOME
from sysconf.lib import logtitle
from sysconf.lib import safe_remove
from sysconf.lib import symlink


def main():
    logtitle("symlink home config files")
    for name in os.listdir(DIR_STATIC_HOME):
        src = os.path.join(DIR_STATIC_HOME, name)
        dst = os.path.join(DIR_HOME, name)
        if name.startswith('.') and os.path.isfile(src):
            safe_remove(dst)
            symlink(src, dst)
