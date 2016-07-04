import os
import textwrap

from sysconf.lib import LINUX
from sysconf.lib import logtitle
from sysconf.lib import sh
from sysconf.lib import skip_if
from sysconf.lib import SkipTask
from sysconf.lib import which


@skip_if(not LINUX)
def main():
    # http://www.ubuntugeek.com/how-to-install-skype-in-ubuntu-12-04precise.html
    if which('skype'):
        raise SkipTask('skype already installed')
    s = textwrap.dedent(""" \
        sudo apt-add-repository "deb http://archive.canonical.com/ $(lsb_release -sc) partner"
        sudo apt-get update
        sudo apt-get install -y skype
    """)
    sh(s)
