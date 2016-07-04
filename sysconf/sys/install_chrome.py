import os
import textwrap

from sysconf.lib import LINUX
from sysconf.lib import sh
from sysconf.lib import skip_if
from sysconf.lib import SkipTask
from sysconf.lib import which


@skip_if(not LINUX)
def main():
    # http://www.ubuntuupdates.org/ppa/google_chrome
    if which('google-chrome'):
        raise SkipTask('chrome already installed')
    s = textwrap.dedent(""" \
        wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
        sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
        sudo apt-get update
        sudo apt-get install -y google-chrome-stable
        """
    )
    sh(s)
