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


# https://github.com/sindresorhus/text-extensions/
SRC_EXTS = set([
    "applescript", "asp", "aspx", "atom", "bashrc", "bat", "bbcolors",
    "bowerrc", "c", "cc", "cfc", "cfg", "cfm", "cmd", "cnf", "coffee", "conf",
    "cpp", "cson", "css", "csslintrc", "csv", "curlrc", "cxx", "diff", "eco",
    "editorconfig", "ejs", "emacs", "eml", "erb", "erl", "eslintignore",
    "eslintrc", "gemrc", "gitattributes", "gitconfig", "gitignore", "go",
    "gvimrc", "h", "haml", "hbs", "hgignore", "hpp", "htaccess", "htm", "html",
    "iced", "ini", "ino", "irbrc", "itermcolors", "jade", "js", "jscsrc",
    "jshintignore", "jshintrc", "json", "jsonld", "jsx", "less", "ls", "log",
    "m", "markdown", "md", "mdown", "mdwn", "mht", "mhtml", "mkd", "mkdn",
    "mkdown", "nfo", "npmrc", "npmignore", "nvmrc", "patch", "pbxproj", "pch",
    "php", "phtml", "pl", "pm", "properties", "py", "rb", "rdoc",
    "rdoc_options", "ron", "rss", "rst", "rtf", "rvmrc", "sass", "scala",
    "scss", "seestyle", "sls", "sss", "sh", "strings", "styl", "stylus",
    "sub", "sublime-build", "sublime-commands", "sublime-completions",
    "sublime-keymap", "sublime-macro", "sublime-menu", "sublime-project",
    "sublime-settings", "sublime-workspace", "svg", "sql", "terminal",
    "text", "textile", "tmLanguage", "tmTheme", "tsv", "txt", "vbs",
    "vim", "viminfo", "vimrc", "webapp", "xht", "xhtml", "xml", "xsl", "yaml",
    "yml", "zsh", "zshrc",
])
# https://github.com/sindresorhus/binary-extensions
BIN_EXTS = set([
    "3ds", "3g2", "3gp", "7z", "a", "aac", "adp", "ai", "aif", "aiff", "alz",
    "ape", "apk", "ar", "arj", "asf", "au", "avi", "bak", "bh", "bin", "bk",
    "bmp", "btif", "bz2", "bzip2", "cab", "caf", "cgm", "class", "cmx", "cpio",
    "cr2", "csv", "cur", "dat", "deb", "dex", "djvu", "dll", "dmg", "dng",
    "doc", "docm", "docx", "dot", "dotm", "dra", "DS_Store", "dsk", "dts",
    "dtshd", "dvb", "dwg", "dxf", "ecelp4800", "ecelp7470", "ecelp9600", "egg",
    "eol", "eot", "epub", "exe", "f4v", "fbs", "fh", "fla", "flac", "fli",
    "flv", "fpx", "fst", "fvt", "g3", "gif", "graffle", "gz", "gzip", "h261",
    "h263", "h264", "ico", "ief", "img", "ipa", "iso", "jar", "jpeg", "jpg",
    "jpgv", "jpm", "jxr", "key", "ktx", "lha", "lvp", "lz", "lzh", "lzma",
    "lzo", "m3u", "m4a", "m4v", "mar", "mdi", "mht", "mid", "midi", "mj2",
    "mka", "mkv", "mmr", "mng", "mobi", "mov", "movie", "mp3", "mp4", "mp4a",
    "mpeg", "mpg", "mpga", "mxu", "nef", "npx", "numbers", "o", "oga", "ogg",
    "ogv", "otf", "pages", "pbm", "pcx", "pdf", "pea", "pgm", "pic", "png",
    "pnm", "pot", "potm", "potx", "ppa", "ppam", "ppm", "pps", "ppsm", "ppsx",
    "ppt", "pptm", "pptx", "psd", "pya", "pyc", "pyo", "pyv", "qt", "rar",
    "ras", "raw", "rgb", "rlc", "rmf", "rmvb", "rtf", "rz", "s3m", "s7z",
    "scpt", "sgi", "shar", "sil", "slk", "smv", "so", "sub", "swf", "tar",
    "tbz", "tbz2", "tga", "tgz", "thmx", "tif", "tiff", "tlz", "ts", "ttc",
    "ttf", "txz", "udf", "uvh", "uvi", "uvm", "uvp", "uvs", "uvu", "viv",
    "vob", "war", "wav", "wax", "wbmp", "wdp", "weba", "webm", "webp", "whl",
    "wim", "wm", "wma", "wmv", "wmx", "woff", "woff2", "wvx", "xbm", "xif",
    "xla", "xlam", "xls", "xlsb", "xlsm", "xlsx", "xlt", "xltm", "xltx", "xm",
    "xmind", "xpi", "xpm", "xwd", "xz", "z", "zip", "zipx",
])
KNOWN_BASENAMES = set([
    'README', 'Makefile', '.gitignore'
])
SHEBANGS = {
    '#!/bin/bash': '.bash',
    '#!/bin/csh -f': '.csh',
    '#!/bin/csh': '.csh',
    '#!/bin/sh': '.sh',
    '#!/usr/bin/env bash': '.bash',
    '#!/usr/bin/env jsc': '.js',
    '#!/usr/bin/env lua': '.lua',
    '#!/usr/bin/env node': '.js',
    '#!/usr/bin/env perl': '.pl',
    '#!/usr/bin/env php': '.php',
    '#!/usr/bin/env python': '.py',
    '#!/usr/bin/env python3': '.py',
    '#!/usr/bin/env rhino': '.js',
    '#!/usr/bin/env ruby': '.rb',
    '#!/usr/bin/lua': '.lua',
    '#!/usr/bin/perl': '.pl',
    '#!/usr/bin/php': '.php',
    '#!/usr/bin/ruby': '.rb',
}
DEBUG = False


# ===================================================================
# utils
# ===================================================================


def sh(cmd):
    return subprocess.check_output(cmd, shell=True).strip()


def log(msg):
    print(msg)


def logdebug(msg):
    if DEBUG:
        print(msg, file=sys.stderr)


def warn(msg):
    print(hilite(msg, color='orange'), file=sys.stderr)


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


def hilite(s, color):
    """Return an highlighted version of 'string'."""
    if not term_supports_colors():
        return s
    attr = []
    if color == 'red':
        attr.append('31')
    elif color == 'green':
        attr.append('32')
    elif color == 'orange':
        attr.append('33')
    else:
        raise ValueError(color)
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), s)


# ===================================================================
# implementation
# ===================================================================


def get_src_files():
    out = subprocess.check_output("git ls-files", shell=True)
    return [x for x in out.split(b'\n') if x]


def get_no_lines(file):
    with open(file, 'rt') as f:
        return len(f.readlines())


def istext(file):
    ext = os.path.splitext(file)[1]
    if ext in SRC_EXTS:
        return True
    if ext in BIN_EXTS:
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
                firstline = f.readline()
                if not firstline:
                    break
                firstline = firstline.strip()
                if firstline:
                    break
            try:
                return SHEBANGS[firstline]
            except KeyError:
                warn("can't recognize file %r" % file)
                return '(no-extension)'


def main():
    # setup
    global DEBUG

    args = docopt(__doc__)
    DEBUG = args['--debug']
    stats = collections.defaultdict(int)
    files = get_src_files()

    # collect stats
    for i, file in enumerate(files):
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
