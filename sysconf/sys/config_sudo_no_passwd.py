import os

from sysconf.lib import LINUX
from sysconf.lib import sh
from sysconf.lib import skip_if


@skip_if(not LINUX)
def main():
    # do not prompt password when using sudo
    s = "$USER ALL=(ALL) NOPASSWD: ALL"
    sh('echo "$USER ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers')
