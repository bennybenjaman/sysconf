#!/usr/bin/env python

"""
Recursively grep (or replaces) occurrences of <str> in all "dev" files
in this directory.  Very similar to "ack" CLI util."

Usage:
    grep.py [-r <str>] [-e <exts>] [-v] <str>

Options:
    -r <str> --replace=<str>  # replace string
    -e <exts> --exts=<exts>   # a list of extensions default=%s
    -v --verbose              # print line occurrences
"""

from __future__ import print_function
import os
import sys

from docopt import docopt

from sysconf.lib import hilite


DEFAULT_EXTS = [
    'c',
    'h',
    'md',
    'py',
    'rst',
    'txt',
]
IGNORE_ROOT_DIRS = [
    '.git',
    'build',
    'dist',
]
__doc__ = __doc__ % str(tuple(DEFAULT_EXTS))


def grep_file(filepath, pattern, replace=None, verbose=False):
    def print_occurrences(data):
        for lineno, line in enumerate(data.splitlines(), 1):
            if pattern in line:
                line = line.replace(pattern, hilite(pattern))
                print("%s: %s" % (hilite(lineno, ok=None, bold=1), line))


    def replace_in_file(data, src, dst):
        new_data = data.replace(src, dst)
        with open(filepath, 'w') as f:
            f.write(new_data)

    with open(filepath, 'r') as f:
        data = f.read()

    occurrences = 0
    if pattern in data:
        occurrences += data.count(pattern)
        print(hilite(filepath, bold=1))
        print_occurrences(data)
        print()
        if replace:
            replace_in_file(data, pattern, replace)

    return occurrences


def main(argv=None):
    # CLI
    args = docopt(__doc__, argv=None)
    if args['--exts']:
        exts = args['--exts'].split(',')
    else:
        exts = DEFAULT_EXTS
    for i, ext in enumerate(exts):
        if not ext.startswith('.'):
            exts[i] = '.' + ext
    exts = set(exts)
    pattern = args['<str>']
    replace = args['--replace']
    verbose = args['--verbose']

    # run
    files_matching = 0
    occurrences = 0
    for root, dirs, files in os.walk('.', topdown=False):
        # skip
        parent_root = os.path.normpath(root).split('/')[0]
        if parent_root in IGNORE_ROOT_DIRS:
            continue
        if parent_root.endswith('.egg-info'):
            continue
        for name in files:
            if os.path.splitext(name)[1] not in exts:
                continue
            filepath = os.path.join(root, name)
            ocs = grep_file(
                filepath, pattern, replace=replace, verbose=verbose)
            occurrences += ocs
            if ocs:
                files_matching += 1

    if occurrences:
        print("occurrences=%s, files-matching=%s" % (
            hilite(occurrences, bold=1),
            hilite(files_matching, bold=1)
        ))


if __name__ == '__main__':
    main()
