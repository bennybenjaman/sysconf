#!/usr/bin/env python

# Copyright (c) 2016 Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license.

# TODO: implement AND logic, not only OR
# TODO: regular expressions?

"""
Recursively search a string occurrence in all files of this directory.
Very similar to "ack" command, just simpler.
Features:
 * simple search
 * case insensitive search
 * search & replacelp
 * logical AND search for multiple patterns on the same line
 * colors
 * open in system editor

Usage:
    grep.py [-r] [-i] [-o] [-n <N>] [-e <EXTS>] <pattern> ...

Options:
    -r --replace              # replace 2 patterns
    -i --ignore-case          # case insensitive
    -e <EXTS> --exts=<EXTS>   # a list of comma separated extensions default=%s
    -o --open                 # open files in editor
    -n <N> --nlines=<N>       # number of lines to print above and below

Examples:
    grep.py -e py,c,h pattern  # search for specific extensions
    grep.py foo bar            # search for 'foo' AND 'bar' on the same line
    grep.py -r foo bar         # replaces 'foo' with 'bar'
    grep.py foo -n 5           # prints the 5 lines before and after the match
    grep.py foo -o             # open matching files in system editor
"""

from __future__ import print_function
import collections
import os
import subprocess
import sys

from docopt import docopt


PY3 = sys.version_info[0] == 3
if PY3:
    basestring = str
    raw_input = input
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


# ===================================================================
# utils
# ===================================================================


try:
    from shutil import which
except ImportError:
    def which(cmd, mode=os.F_OK | os.X_OK, path=None):
        """Given a command, mode, and a PATH string, return the path which
        conforms to the given mode on the PATH, or None if there is no such
        file.

        `mode` defults to os.F_OK | os.X_OK. `path` defults to the result
        of os.environ.get("PATH"), or can be overridden with a custom search
        path.
        """
        def _access_check(fn, mode):
            return (os.path.exists(fn) and os.access(fn, mode) and
                    not os.path.isdir(fn))

        if os.path.dirname(cmd):
            if _access_check(cmd, mode):
                return cmd
            return None

        if path is None:
            path = os.environ.get("PATH", os.defpath)
        if not path:
            return None
        path = path.split(os.pathsep)

        if sys.platform == "win32":
            if os.curdir not in path:
                path.insert(0, os.curdir)

            pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
            if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
                files = [cmd]
            else:
                files = [cmd + ext for ext in pathext]
        else:
            files = [cmd]

        seen = set()
        for dir in path:
            normdir = os.path.normcase(dir)
            if normdir not in seen:
                seen.add(normdir)
                for thefile in files:
                    name = os.path.join(dir, thefile)
                    if _access_check(name, mode):
                        return name
        return None


def get_terminal_size():
    try:
        # Added in Python 3.3
        from shutil import get_terminal_size as gts
    except ImportError:
        try:
            # This should work on Linux.
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
def get_editor_cmd():
    # always give precedence to sublime (sorry!)
    if which("subl"):
        return ["subl"]
    else:
        default = os.getenv("EDITOR")
        if default:
            return [default]
        else:
            if which("vim"):
                return ["vim"]
            elif which("vi"):
                return ["vi"]
            else:
                sys.exit("no editor found")


@memoize
def term_supports_colors(file=sys.stdout):
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
    if not term_supports_colors():
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


def exit(msg):
    print(hilite(msg, ok=False), file=sys.stderr)
    sys.exit(1)


def open_file(path):
    cmd = get_editor_cmd()
    subprocess.call(cmd + [path])


# ===================================================================
# implementation
# ===================================================================


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
                    hilite(curr_pos + 1, ok=None, bold=True), line.rstrip()))
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
                    hilite(curr_pos + 1, ok=None, bold=True),
                    line.rstrip()))
            finally:
                curr_pos += 1

    def find_occurrences(lines, patterns):
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
                    print(hilite(filepath, bold=True))
                    header_printed = True
                # Print the N lines previous to this match.
                if nlines:
                    print_pre_lines(lines, lineno - 1)
                # Note: if case-sensitive, this may not highlight the
                # line (well... who cares =)).
                for pattern in patterns:
                    line = line.replace(pattern, hilite(pattern))
                print("%s: %s" % (
                    hilite(lineno, ok=None, bold=True), line.rstrip()))
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
            occurrences += find_occurrences(lines, patterns)
        return occurrences

    def find_multi_patterns(patterns):
        assert isinstance(patterns, list)
        if replace and len(patterns) != 2:
            exit("with --replace you must specifcy 2 <pattern>s")
        with open(filepath, 'r') as f:
            occurrences = find_occurrences(f, set(patterns))
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
                hilite(filepath, bold=True), hilite(occurrences)))
            with open(filepath, 'w') as f:
                f.write(new_data)
        return occurrences

    if ignore_case:
        patterns = [x.lower() for x in patterns]

    if len(set(patterns)) != len(patterns):
        exit("<pattern>s can't be equal")
    elif len(patterns) == 1 and not ignore_case:
        return find_single_pattern(patterns[0])
    elif len(patterns) == 2 and replace:
        if ignore_case:
            exit("can't user --ignore-case with --replace")
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
            exit("invalid extension %s" % ext)
        if not ext.startswith('.'):
            exts[i] = '.' + ext
    exts = set(exts)
    patterns = args['<pattern>']
    replace = args['--replace']
    ignore_case = args['--ignore-case']
    nlines = int(args['--nlines']) if args['--nlines'] else 0
    start_ext = exts == set(['.*'])

    # Run.
    files_matching = []
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
                exts_map[ext] += 1
                files_matching.append(filepath)

    if occurrences:
        # Print final stats.
        exts_stats = []
        for k, v in sorted(exts_map.items(), key=lambda v: v[1], reverse=1):
            exts_stats.append("%s=%s" % (k, hilite(v)))

        print("occurrences=%s, files-matching=%s, exts=(%s)" % (
            hilite(occurrences, bold=True),
            hilite(len(files_matching), bold=True),
            ','.join(exts_stats),
        ))

        if args['--open']:
            if len(files_matching) == 1:
                open_file(files_matching.pop())
            else:
                for i, file in enumerate(files_matching, 1):
                    print("%s: %s" % (
                        hilite(str(i), ok=None, bold=True), file))
                while True:
                    sel = raw_input('open file (* for all): ')
                    if sel.isdigit() or sel == '*':
                        break
                if sel == '*':
                    for file in files_matching:
                        open_file(file)
                else:
                    open_file(files_matching[int(sel) - 1])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
