#!/usr/bin/env python

"""
Recursively replaces occurrences of a string in this dir.

Usage:
    rreplace.py [--write] [--exts=<exts>]<src> <dst>

Options:
    -e <exts> --exts=<exts>   # a list of extensions default=%s
    -w --write                # write changes
"""

import os
import sys

from docopt import docopt


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


def replace(filepath, src, dst, write):
    with open(filepath, 'r') as f:
        data = f.read()
    replaced = data.replace(src, dst)
    if data != replaced:
        occurrences = data.count(dst)
        if write:
            print("updating %-3s occurrences in %s" % (occurrences, filepath))
            # with open(file, 'w') as f:
            #     f.write(replaced)
        else:
            print("found %-3s occurrences in %s" % (occurrences, filepath))



def main():
    # CLI
    args = docopt(__doc__)
    if args['--exts']:
        exts = args['--exts'].split(',')
    else:
        exts = DEFAULT_EXTS
    for i, ext in enumerate(exts):
        if not ext.startswith('.'):
            exts[i] = '.' + ext
    exts = set(exts)
    src = args['<src>']
    dst = args['<dst>']
    write = args['--write']

    # run
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
            replace(filepath, src, dst, write)


if __name__ == '__main__':
    main()
