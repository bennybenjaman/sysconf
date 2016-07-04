"""
Install system packages.
"""

import os
import subprocess

from sysconf.lib import logtitle
from sysconf.lib import LINUX
from sysconf.lib import install_pkg
from sysconf.lib import sh


def pkg_linux():
    BASE = ["msttcorefonts", "vim", "",
            "ubuntu-restricted-extras", "rar", "unrar"]
    ADMIN = ["screen", "htop", "virtualbox", "curl", "realpath"]
    DEV = ["mercurial", "git", "colordiff", "libreadline-dev",
           "libncurses*-dev", "python-dev", "python3-dev", "ack-grep",
           "build-essential", "libffi-dev", "libssl-dev"]
    GUIS = ["gcolor2", "vlc"]
    SYS = ["xawtv"]
    EXTRA = ["indicator-cpufreq"]
    EXTRA.append(
        subprocess.check_output(
            "echo linux-headers-`uname -r`", shell=1).strip())

    ALL = BASE + ADMIN + DEV + GUIS + SYS + EXTRA
    install_pkg(*ALL)



def main():
    logtitle("install system base packages")
    if LINUX:
        pkg_linux()
