from sysconf.lib import LINUX
from sysconf.lib import skip_if
from sysconf.lib import sh
from sysconf.lib import str_in_file


@skip_if(not LINUX)
def main():
    if not str_in_file("enabled=0", "/etc/default/apport"):
        sh('echo "enabled=0" | sudo tee -a /etc/default/apport')
