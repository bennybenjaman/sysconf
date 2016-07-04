from sysconf.lib import LINUX
from sysconf.lib import skip_if
from sysconf.lib import uninstall_pkg


@skip_if(not LINUX)
def main():
    uninstall_pkg(*['gedit', 'totem'])
