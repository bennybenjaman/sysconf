#!/usr/bin/env python

# TODO: case-insnsitive

"""
Recursively grep (or replaces) occurrences of <str> in all "dev" files
in this directory.  Very similar to "ack" CLI util."

Usage:
    grep.py [-e <exts>] [-r] [<pattern> ...]

Options:
    -e <exts> --exts=<exts>   # a list of extensions default=%s
    -r --replace              # replace 2 patterns

Examples:
    grep.py -e py,c,h pattern    # extensions
    grep.py foo bar              # search for 'foo' and 'bar' on the same line
    grep.py -r foo bar           # replaces 'foo' with 'bar'
"""

from __future__ import print_function
import os
import sys

from docopt import docopt

from sysconf import hilite


DEFAULT_EXTS = [
    'c',
    'h',
    'in',
    'ini',
    'md',
    'py',
    'rst',
    'txt',
    'yaml',
    'yml',
]
SPECIAL_NAMES = [
    'README',
]
IGNORE_ROOT_DIRS = [
    '.git',
    'build',
    'dist',
]
__doc__ = __doc__ % str(tuple(DEFAULT_EXTS))


def grep_file(filepath, patterns, replace=False):
    def print_occurrences(lines, patterns):
        if not isinstance(lines, list):
            # probably a file object
            lines = iter(lines)
        occurrences = 0
        header_printed = False
        for lineno, line in enumerate(lines, 1):
            for pattern in patterns:
                if pattern not in line:
                    break
            else:
                if not header_printed:
                    print(hilite(filepath, bold=1))
                    header_printed = True
                for pattern in patterns:
                    line = line.replace(pattern, hilite(pattern))
                print("%s: %s" % (
                    hilite(lineno, ok=None, bold=1), line.strip()))
                occurrences += 1
        if occurrences:
            print()
        return occurrences

    def replace_in_file(data, src, dst):
        new_data = data.replace(src, dst)
        with open(filepath, 'w') as f:
            f.write(new_data)

    def find_single_pattern(pattern):
        assert isinstance(pattern, basestring)
        with open(filepath, 'r') as f:
            data = f.read()
        occurrences = 0
        if pattern in data:
            lines = data.splitlines()
            occurrences += print_occurrences(lines, patterns)
        return occurrences

    def find_multi_patterns(patterns):
        assert isinstance(patterns, list)
        assert not replace
        if replace and len(patterns) != 2:
            sys.exit("with --replace you must specifcy 2 <pattern>s")
        with open(filepath, 'r') as f:
            return print_occurrences(f, patterns)
        if replace:
            with open(filepath, 'r') as f:
                data = f.read()
            replace_in_file(data, pattern, replace)


        # if replace:
        #     replace_in_file(data, pattern, replace)

    if len(patterns) == 1:
        return find_single_pattern(patterns[0])
    else:
        return find_multi_patterns(patterns)


def main(argv=None):
    # CLI
    args = docopt(__doc__, argv=None)
    if args['--exts']:
        exts = args['--exts'].split(',')
    else:
        exts = DEFAULT_EXTS
    for i, ext in enumerate(exts):
        if not ext.isalnum() and ext != '*':
            sys.exit("invalid extension %s" % ext)
        if not ext.startswith('.'):
            exts[i] = '.' + ext
    exts = set(exts)

    patterns = args['<pattern>']
    replace = False

    # run
    start_ext = exts == set(['.*'])
    files_matching = 0
    occurrences = 0
    for root, dirs, files in os.walk('.', topdown=False):
        parent_root = os.path.normpath(root).split('/')[0]
        if parent_root in IGNORE_ROOT_DIRS:
            continue  # skip
        if parent_root.endswith('.egg-info'):
            continue  # skip
        for name in files:
            if os.path.splitext(name)[1] not in exts:
                if name not in SPECIAL_NAMES:
                    if not start_ext:
                        continue   # skip
            filepath = os.path.join(root, name)
            ocs = grep_file(
                filepath, patterns, replace=replace)
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
