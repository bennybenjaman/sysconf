#!/usr/bin/env python

# Copyright (c) 2016 Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license.

"""
Print statistics about a code project.

Usage:
    codestats.py [-d]

Options:
    -d --debug         # print debug output
"""

from __future__ import print_function, division
import collections
import os
import subprocess
import string
import sys

from docopt import docopt  # requires 'pip install docopt'


KNOWN_SRC_EXTS = {'.py', '.html', '.css', '.c', '.h', 'cpp'}
KNOWN_BIN_EXTS = {'.pyc', '.pyo', '.pyd', '.so', '.png', '.jpg'}
KNOWN_BASENAMES = {'README', 'Makefile'}
DEBUG = False


def sh(cmd):
    return subprocess.check_output(cmd, shell=True).strip()


def log(msg):
    print(msg)


def logdebug(msg):
    if DEBUG:
        print(msg, file=sys.stderr)


def get_src_files():
    out = subprocess.check_output("git ls-files", shell=True)
    return [x for x in out.split(b'\n') if x]


def get_no_lines(file):
    with open(file, 'rt') as f:
        return len(f.readlines())


def istext(file):
    ext = os.path.splitext(file)[1]
    if ext in KNOWN_SRC_EXTS:
        return True
    if ext in KNOWN_BIN_EXTS:
        return False

    s = open(file).read(512)
    text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
    null_trans = string.maketrans("", "")
    if not s:
        # Empty files are considered text
        return True
    if "\0" in s:
        # Files with null bytes are likely binary
        return False
    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(null_trans, text_characters)
    # If more than 30% non-text characters, then
    # this is considered a binary file
    if float(len(t)) / float(len(s)) > 0.30:
        return False
    return True


def get_file_ext(file):
    ext = os.path.splitext(file)[1]
    if ext:
        return ext
    else:
        # guess by file name
        name = os.path.basename(file)
        if name in KNOWN_BASENAMES:
            return name
        # guess by shebang
        with open(file, 'rt') as f:
            while True:
                firstline = f.readline().strip()
                if firstline:
                    break
            if not firstline.startswith('#'):
                return '?'
            if firstline.startswith('#!/usr/bin/env python'):
                return '.py'
            if 'bash' in firstline or 'sh' in firstline:
                return '.sh'
            logdebug("can't recognize file %r" % file)
            return '?'


def main():
    # setup
    global DEBUG
    args = docopt(__doc__)
    DEBUG = args['--debug']
    stats = collections.defaultdict(int)
    files = get_src_files()

    # collect stats
    for file in files:
        if not istext(file):
            continue
        ext = get_file_ext(file)
        stats[ext] += get_no_lines(file)

    # calculate percent
    percent = {}
    tot_lines = sum(stats.values())
    for ext, lines in stats.items():
        percent[ext] = round(lines / tot_lines * 100, 1)

    # print stats
    print("-" * 34)
    print("ext                 lines        %")
    print("-" * 34)
    pairs = sorted(stats.items(), key=lambda (k, v): v, reverse=True)
    for ext, lines in pairs:
        print("%-18s %6s %7s%%" % (ext, lines, percent[ext]))
    print("-" * 34)
    print("lines:        %20s" % tot_lines)
    print("files:        %20s" % len(files))
    print("commits:      %20s" % sh("git rev-list --all --count"))
    print("committers:   %20s" % len(sh("git shortlog -sn").split('\n')))


main()
