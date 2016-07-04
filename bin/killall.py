#!/usr/bin/env python

"""
Kill a process by name.

Usage:
    killall.py [-d] <name>

Options:
    -d --dryrun     # just print processes matchin <name> without killing
"""

import os
import signal
import sys
import psutil

from docopt import docopt

from sysconf import hilite


THIS_PID = os.getpid()


def logerr(s):
    print(hilite(s, ok=False))



def find_procs(name):
    procs = []
    for p in psutil.process_iter():
        if p.pid != THIS_PID:
            try:
                p_name = p.name()
                p_cmdline = p.cmdline()
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                logerr("access denied: %s" % p)
            else:
                if name in p_name or name in ' '.join(p_cmdline):
                    procs.append(p)
    return procs


def main():
    args = docopt(__doc__)
    name = args['<name>']

    # get procs matching criteria
    procs = find_procs(name)
    if not procs:
        return

    # send SIGTERM
    signaled = []
    for p in procs:
        try:
            p.terminate()
        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            logerr("SIGTERM access denied: %s" % p)
        else:
            print("SIGTERM %s" % p)
            signaled.append(p)
    if not signaled:
        return

    gone, alive = psutil.wait_procs(signaled, 3)

    signaled = []
    for p in alive:
        try:
            p.kill()
        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            logerr("SIGKILL access denied: %s" % p)
        else:
            print("SIGKILL %s" % p)
            signaled.append(p)

    gone, alive = psutil.wait_procs(signaled, 3)
    if alive:
        logerr("the following processes survived even SIGKILL!")
        for p in alive:
            logerr(p)
        sys.exit(1)


if __name__ == '__main__':
    main()

