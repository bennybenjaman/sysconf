#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license.

"""\
Look for broken urls in files.

Usage:
    find_broken_links.py [-v] [-t <secs>] <file>...

Options:
    -v --verbose           # more verbose output
    -t --timeout <secs>    # HTTP request timeout

Example for checking all text files of a GIT project:
    git grep --cached -Il '' | xargs find_broken_links.py
"""


from __future__ import print_function
import os
import re
import socket
import sys
from concurrent.futures import ThreadPoolExecutor
try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

from docopt import docopt


SOCKET_TIMEOUT = 5
VERBOSE = False
DONE = 0


def term_supports_colors():
    try:
        import curses
        assert sys.stderr.isatty()
        curses.setupterm()
        assert curses.tigetnum("colors") > 0
    except Exception:
        return False
    else:
        return True


if term_supports_colors():
    def hilite(s, ok=True, bold=False):
        """Return an highlighted version of 'string'."""
        attr = []
        if ok is None:  # no color
            pass
        elif ok:   # green
            attr.append('32')
        else:   # red
            attr.append('31')
        if bold:
            attr.append('1')
        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), s)
else:
    def hilite(s, *a, **kw):
        return s


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]'
        '{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(re.match(regex, url))


def find_urls(file):
    with open(file, 'r') as f:
        data = f.read()
    regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%' \
            '[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(regex, data)
    for url in urls:
        url = url.rstrip("/>")
        url = url.rstrip(".")
        url = url.rstrip(",")
        url = url.rstrip("'")
        url = url.rstrip(")")
        if is_valid_url(url):
            yield url


def try_url(url, total):
    global DONE

    class HeadRequest(Request):
        def get_method(self):
            return "HEAD"

    err = None
    try:
        resp = urlopen(HeadRequest(url))
    except Exception as err:
        return str(err)
    else:
        if resp.code != 200:
            return "code == %s" % resp.code
    finally:
        DONE += 1


def main(argv=None):
    # setup
    global VERBOSE
    args = docopt(__doc__, argv=argv)
    files = args['<file>']
    timeout = int(args['--timeout'] or 0) or SOCKET_TIMEOUT
    VERBOSE = args['--verbose']
    socket.setdefaulttimeout(timeout)
    urls = set()

    # find urls
    for file in files:
        for url in find_urls(file):
            urls.add(url)
    urls = sorted(urls)

    # inspect them
    futs = {}
    urls = sorted(urls)
    with ThreadPoolExecutor(max_workers=200) as ex:
        for url in urls:
            futs[url] = ex.submit(try_url, url, len(urls))

    # done, print results
    for url in urls:
        err = futs[url].result()
        if err:
            print("%s %s" % (url, hilite(err, ok=False)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        os._exit(0)  # quick & dirty way to kill the thread pool
