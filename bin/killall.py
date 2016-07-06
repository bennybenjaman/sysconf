#!/usr/bin/env python

"""
Kill a process by name.

Usage:
    killall.py [-d] [-t] [-v] <name>

Options:
    -d --dryrun     # just print processes matchin <name> without killing
    -t --timeout    # how much to wait for proc to die
    -v --verbose    # print more info about the process
"""

from __future__ import print_function

import collections
import os
import signal
import sys
import psutil

from docopt import docopt

from sysconf import hilite


THIS_PID = os.getpid()
PY3 = sys.version_info[0] == 3
TIMEOUT = 1
ntproc = collections.namedtuple('Process', 'pid name status ppid parent')


def logerr(s):
    print(hilite(s, ok=False))


def str_proc(p):
    if VERBOSE:
        import pprint
        info = p.as_dict(
            ['pid', 'ppid', 'name', 'cmdline', 'status', 'username'])
        info['cmdline'] = ' '.join(info['cmdline'])
        par = p.parent()
        if par:
            info['parent'] = par.name()
        return "Process(%s)" % pprint.pformat(info)
    else:
        par = p.parent()
        parname = par.name() if par is not None else None
        return str(ntproc(p.pid, p.name(), p.status(), p.ppid(), parname))


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
                    p.strrepr = str_proc(p)
                    procs.append(p)
    return procs


def stringify_sig(signum):
    if not PY3:
        smap = dict([(getattr(signal, x), x) for x in dir(signal)
                     if x.startswith('SIG')])
        return smap.get(signum, signum)
    else:
        return signum


def main():
    global VERBOSE

    def signal_proc(p, sig):
        strsig = stringify_sig(sig)
        try:
            p.send_signal(sig)
        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            logerr("%s access denied: %s" % (strsig, p))
        else:
            print("%s %s" % (strsig, p.strrepr))
            signaled.append(p)

    def gone_callback(p):
        print(hilite("%s is gone" % p.strrepr))

    def wait_procs_and_exit(procs):
        if not procs:
            sys.exit(0)
        gone, alive = psutil.wait_procs(
            procs, timeout=timeout, callback=gone_callback)
        if not alive:
            sys.exit(0)
        return alive

    args = docopt(__doc__)
    name = args['<name>']
    dryrun = args['--dryrun']
    timeout = args['--timeout'] or TIMEOUT
    VERBOSE = args['--verbose']

    # get procs matching criteria
    procs = find_procs(name)
    if not procs:
        return

    # dry run
    if dryrun:
        for p in procs:
            print(str_proc(p))
        return

    # send SIGTERM
    signaled = []
    for p in procs:
        signal_proc(p, signal.SIGTERM)
    still_alive = wait_procs_and_exit(signaled)

    # send SIGKILL
    print()
    signaled = []
    for p in procs:
        signal_proc(p, signal.SIGKILL)
    still_alive = wait_procs_and_exit(signaled)

    #
    print()
    logerr("the following processes survived even SIGKILL!")
    for p in still_alive:
        logerr(p.strrepr)
    sys.exit(1)


if __name__ == '__main__':
    main()
