#!/usr/bin/env python

# Copyright (c) 2016 Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# TODO: may want to implement also the AND logic, not only OR

"""
Recursively search a string in all directory files.
Very similar to "ack" command.

Usage:
    grep.py [-e <exts>] [-r] [-i] [-n <lines>] [<pattern> ...]

Options:
    -r --replace              # replace 2 patterns
    -i --ignore-case          # case insensitive
    -e <exts> --exts=<exts>   # a list of extensions defult=%s
    -n <lines> --nlines=<lines>  # number of lines to print above and below

Examples:
    grep.py -e py,c,h pattern    # extensions
    grep.py foo bar              # search for 'foo' AND 'bar' on the same line
    grep.py -r foo bar           # replaces 'foo' with 'bar'
    grep.py foo -n 5             # prints also the 5 pre and post lines
"""

from __future__ import print_function
import collections
import os
import sys

from docopt import docopt


PY3 = sys.version_info[0] == 3
TERMINAL_SIZE_FALLBACK = 2
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


def get_terminal_size():
    try:
        from shutil import get_terminal_size as gts
    except ImportError:
        try:
            import fcntl
            import termios
            import struct
            hw = struct.unpack('hh', fcntl.ioctl(
                1, termios.TIOCGWINSZ, '1234'))
            return hw[1]
        except Exception:
            return TERMINAL_SIZE_FALLBACK
    else:
        gts(fallback=(TERMINAL_SIZE_FALLBACK, 0))[0]


TERMINAL_SIZE = get_terminal_size()


def memoize(f):
    """Memoize function or method return values, saving time if
    method has already been called with that same argument.
    """
    cache = {}

    def memf(*x):
        if x not in cache:
            cache[x] = f(*x)
        return cache[x]
    return memf


@memoize
def _term_supports_colors(file=sys.stdout):
    try:
        import curses
        assert file.isatty()
        curses.setupterm()
        assert curses.tigetnum("colors") > 0
    except Exception:
        return False
    else:
        return True


def hilite(s, ok=True, bold=False):
    """Return an highlighted version of 'string'."""
    if not _term_supports_colors():
        return s
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


def grep_file(filepath, patterns, replace=False, ignore_case=False,
              nlines=0):
    def get_file_content():
        with open(filepath, 'r') as f:
            data = f.read()
        if ignore_case:
            data = data.lower()
        return data

    def print_pre_lines(lines, orig_pos):
        curr_pos = orig_pos - nlines
        print("." * TERMINAL_SIZE)
        while curr_pos < 0 or curr_pos < orig_pos:
            try:
                if curr_pos < 0:
                    continue
                line = lines[curr_pos]
            except KeyError:
                pass
            else:
                print("%s: %s" % (
                    hilite(curr_pos + 1, ok=None, bold=1), line.rstrip()))
            finally:
                curr_pos += 1

    def print_post_lines(lines, orig_pos):
        curr_pos = orig_pos
        exit_at = curr_pos + nlines
        while curr_pos != exit_at:
            try:
                if curr_pos < 0:
                    continue
                line = lines[curr_pos]
            except IndexError:
                # We reached the end of lines
                break
            else:
                print("%s: %s" % (
                    hilite(curr_pos + 1, ok=None, bold=1), line.rstrip()))
            finally:
                curr_pos += 1

    def print_occurrences(lines, patterns):
        if not isinstance(lines, list):
            # probably a file object
            lines = list(lines)
        occurrences = 0
        header_printed = False
        for lineno, line in enumerate(lines, 1):
            for pattern in patterns:
                # lowercase() the line on the fly, but we want to keep
                # the original one around in order to print it.
                temp_line = line if not ignore_case else line.lower()
                if pattern not in temp_line:
                    break
            else:
                if not header_printed:
                    print(hilite(filepath, bold=1))
                    header_printed = True
                # Print the N lines previous to this match.
                if nlines:
                    print_pre_lines(lines, lineno - 1)
                # Note: if case-sensitive, this may not highlight the
                # line (well... who cares =)).
                for pattern in patterns:
                    line = line.replace(pattern, hilite(pattern))
                print("%s: %s" % (
                    hilite(lineno, ok=None, bold=1), line.rstrip()))
                # Print the N lines post to this match.
                if nlines:
                    print_post_lines(lines, lineno)
                occurrences += 1
        if occurrences:
            print()
        return occurrences

    def find_single_pattern(pattern):
        assert isinstance(pattern, basestring)
        data = get_file_content()
        occurrences = 0
        if pattern in data:
            lines = data.splitlines()
            occurrences += print_occurrences(lines, patterns)
        return occurrences

    def find_multi_patterns(patterns):
        assert isinstance(patterns, list)
        if replace and len(patterns) != 2:
            sys.exit("with --replace you must specifcy 2 <pattern>s")
        with open(filepath, 'r') as f:
            occurrences = print_occurrences(f, set(patterns))
        return occurrences

    def replace_patterns(patterns):
        with open(filepath, 'r') as f:
            data = f.read()
        src, dst = patterns
        new_data = data.replace(src, dst)
        occurrences = 0
        if data != new_data:
            occurrences = data.count(src)
            print("%s (%s occurrences)" % (
                hilite(filepath, bold=1), hilite(occurrences)))
            with open(filepath, 'w') as f:
                f.write(new_data)
        return occurrences

    if ignore_case:
        patterns = [x.lower() for x in patterns]
    if len(set(patterns)) != len(patterns):
        sys.exit("<pattern>s can't be equal")
    if len(patterns) == 1 and not ignore_case:
        return find_single_pattern(patterns[0])
    if len(patterns) == 2 and replace:
        if ignore_case:
            sys.exit("can't user --ignore-case with --replace")
        return replace_patterns(patterns)
    else:
        return find_multi_patterns(patterns)


def main(argv=None):
    # CLI parsing.
    args = docopt(__doc__, argv=argv)
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
    replace = args['--replace']
    ignore_case = args['--ignore-case']
    nlines = int(args['--nlines']) if args['--nlines'] else 0
    start_ext = exts == set(['.*'])

    # Run.
    files_matching = 0
    occurrences = 0
    exts_map = collections.defaultdict(int)
    for root, dirs, files in os.walk('.', topdown=False):
        parent_root = os.path.normpath(root).split('/')[0]
        if parent_root in IGNORE_ROOT_DIRS and os.path.isdir(parent_root):
            continue  # skip
        if parent_root.endswith('.egg-info'):
            continue  # skip
        for name in files:
            ext = os.path.splitext(name)[1]
            if ext not in exts:
                if name not in SPECIAL_NAMES:
                    if not start_ext:
                        continue   # skip
            filepath = os.path.join(root, name)
            ocs = grep_file(
                filepath, patterns,
                replace=replace, ignore_case=ignore_case, nlines=nlines)
            occurrences += ocs
            if ocs:
                files_matching += 1
                exts_map[ext] += 1

    if occurrences:
        # Print final stats.
        exts_stats = []
        for k, v in sorted(exts_map.items(), key=lambda v: v[1], reverse=1):
            exts_stats.append("%s=%s" % (k, hilite(v)))

        print("occurrences=%s, files-matching=%s, exts=(%s)" % (
            hilite(occurrences, bold=1),
            hilite(files_matching, bold=1),
            ','.join(exts_stats),
        ))


if __name__ == '__main__':
    main()
