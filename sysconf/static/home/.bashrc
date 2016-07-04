#!/usr/bin/env bash

# ===========================================================================
# Extracted from default Ubuntu's .bashrc
# ===========================================================================

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# append to the history file, don't overwrite it
shopt -s histappend

# don't put duplicate lines or lines starting with space in the history.
HISTCONTROL=ignoreboth

# Make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes
if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    color_prompt=yes
    else
    color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# if this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
    if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
    elif [ -f /etc/bash_completion ]; then
      . /etc/bash_completion
    fi
fi

# --- end

# ===========================================================================
# Set / Export
# ===========================================================================

# constants
_LAPTOP="UX32VD" # laptop id
_HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"  # this dir

# ~/bin is now in the list of exec dirs
PATH="$HOME/bin:$PATH"

# ...so is our revisioned bin dir
PATH="$_HERE/bin:$PATH"

# set English (instead of Italian) for commands output
#export LANG=en_US.UTF-8

# don't use ^D to exit
set -o ignoreeof

# set default programs
if type -P vim > /dev/null; then
    export EDITOR="vim"
    export VISUAL="vim"
else
    export EDITOR="vi"
    export VISUAL="vi"
fi
export PAGER="less"

# save the history of multiple shells in a single file, see:
# http://unix.stackexchange.com/questions/1288
export HISTCONTROL=ignoredups:erasedups  # no duplicate entries
export HISTSIZE=100000                   # big big history
export HISTFILESIZE=100000               # big big history
shopt -s histappend                      # append to history, don't overwrite it
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"

# http://code.activestate.com/recipes/578098-python-interpreter-auto-completion-and-history/
export PYTHONSTARTUP=~/.pythonstart

# man colors
export LESS_TERMCAP_mb=$'\E[01;31m'
export LESS_TERMCAP_md=$'\E[01;38;5;74m'
export LESS_TERMCAP_me=$'\E[0m'
export LESS_TERMCAP_se=$'\E[0m'
export LESS_TERMCAP_so=$'\E[38;5;246m'
export LESS_TERMCAP_ue=$'\E[0m'
export LESS_TERMCAP_us=$'\E[04;38;5;146m'

# ===========================================================================
# Aliases
# ===========================================================================

# ls (also see: http://www.noah.org/engineering/dotfiles/.bashrc)
if [[ $OSTYPE == *linux* ]]; then
    alias ls='ls -hF --color --group-directories-first --time-style=+"%Y-%m-%d %H:%M"'
else
    export CLICOLOR=1
    alias ls='ls -hF'
fi
alias l='ls'
alias ll='ls -l'
alias ls-ext='ls -lXB'        # sort by extension
alias ls-biggest='BLOCKSIZE=1048576; du -x | sort -nr | head -20 | grep -v \.hg | grep -v \.git '
alias ls-size='ls -lSr'        # sort by size
alias ls-hidden='ls -a'        # show hidden files
alias ls-date='ls -ltr'        # sort by date
alias ls-tree='tree -Cs'        # nice alternative to 'ls'
alias ls-dirs='ls -l | grep "^d"'   #list only directories
alias ls-files='ls -l | grep -v "^d"'   #list only file

# navigation
alias ..='cd ..'
alias cd..='cd ..'

# automatically do an ls after each cd
function cd() {
    if [ -n "$1" ]; then
        builtin cd "$@" && ls
    else
        builtin cd ~ && ls
    fi

    if [ -d .git ]; then
        sh-terminal-git
    else
        sh-terminal-default
    fi
}

# dev
alias g='git'
alias git-ci-push='git ci -a -m "progress" && git push'
alias git-pull='git pull -u -v'
alias hg-ci-push='hg ci -m "progress" && hg push'
alias hg-pull='hg pull -u -v'

# saner svn diff
function svn() {
    case $* in
        diff* ) shift 1; command svn diff | less -R ;;
        * ) command svn "$@" ;;
    esac
}

# command substitution
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
# if [ `hostname` = $_LAPTOP ]; then
#     if [ -d ~/.local/share/Trash/files ]; thend
#         alias rm='mv -t ~/.local/share/Trash/files'
#     fi
# fi
alias df='df -h'
alias du='du -h -c'
if [[ $OSTYPE == *linux* ]]; then
    alias grep='grep --color=auto --exclude=*.pyc --exclude=*.orig --exclude=*.rej --exclude-dir=.svn --exclude-dir=.egg-info --exclude-dir=.hg --exclude-dir=.git'
fi
alias reload='source ~/.bashrc'  # 'real' reload is a trap
alias wget='wget -N --no-check-certificate'  # overwrite, don't check SSL cert
alias ssh='ssh -o StrictHostKeyChecking=no'  # don't propt "are you sure...?"

# shutdown / restart / suspend
alias shutdown-now='sudo shutdown -h now'
alias shutdown-restart='sudo shutdown -r now'
alias shutdown-suspend='sudo pm-suspend'

alias s='subl'

# editor
if type -P vim > /dev/null; then
    alias vi="vim"
fi

# =============================================================================
# User defined utility functions start here.
# All starts with "sh-" namespace so that I can distinguish the ones
# defined by me
# =============================================================================

# Add sysconf bin dir to PATH.
SYSCONF_BIN_DIR="$(python -c 'import sysconf.lib; print(sysconf.lib.DIR_BIN)')"
PATH=$PATH:$SYSCONF_BIN_DIR

# net
alias sh-netstat-listen='sudo netstat -antp | grep LISTEN'
alias sh-ping-google='ping google.com'


# =============================================================================
# Dev / Python
# =============================================================================

# try to find a virtualenv and activate it
function sh-py-source-venv() {
    if [ -f venv/bin/activate ]; then
        source venv/bin/activate
    elif [ -f .venv/bin/activate ]; then
        source .venv/bin/activate
    elif [ -f _venv/bin/activate ]; then
        source _venv/bin/activate
    elif [ -f virtualenv/bin/activate ]; then
        source virtualenv/bin/activate
    else
        echo "can't find any virtual env"
    fi
}

# install python for the given python version
function sh-py-install-pip() {
    if [ -z "$1" ] ; then
        echo "usage: py-install-pip <python>"
        return
    fi

    # python 2.4 and 2.5
    if [ $1 = "python2.4" ] || [ $1 = "python2.5" ]; then
        sh-httpfetch https://bitbucket.org/pypa/setuptools/raw/bootstrap-py24/ez_setup.py > /tmp/ez_setup.py
        sudo $1 /tmp/ez_setup.py
        if [ $1 = "python2.4" ]; then
            sudo easy_install-2.4 pip==1.1
        else
            sudo easy_install-2.5 pip==1.1
        fi
    # python 2.6+
    else
        sh-httpfetch https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py
        if [ "$(id -u)" == "0" ]; then
            $1 /tmp/get-pip.py
        else
            sudo $1 /tmp/get-pip.py
        fi
    fi
}

# print all python module imports
function sh-py-find-imports() {
    python << END
if 1:
    import os, fnmatch, re

    def find_imports(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if "import " in line:
                    if line.startswith("from"):
                        m = re.search("^from [a-zA-Z0-9\._]+ import ", line)
                        yield m.group(0).replace(
                            "from ", "").replace(" import", "").strip()
                    else:
                        for x in line[6:].split(','):
                            yield x.strip()

                    #if line.startswith("import") or line.startswith("from"):
                    #    yield line

    found = set()
    for root, dirnames, filenames in os.walk('.'):
        for name in fnmatch.filter(filenames, '*.py'):
            path = os.path.join(root, name)
            if not path.startswith('./.'):  # hidden dirs
                imps = find_imports(path)
                for line in imps:
                    found.add(line)
    print("\n".join(sorted(found)))
END
}

# install pip and ipdb for all installed python versions
function sh-py-setup-all() {
    python << END
if 1:
    import subprocess, os, urllib2

    VERSIONS = ("2.6", "2.7", "3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6")
    IS_ROOT = os.getuid() == 0

    def wget(url, dest):
        data = urllib2.urlopen(url).read()
        dest = os.path.expanduser(dest)
        with open(dest, 'w') as f:
            f.write(data)

    def which(program):
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    def banner(s):
        print("=" * 80)
        print(s)
        print("=" * 80)

    def section(s):
        print(s)
        print("." * len(s))

    def can_import(modname, pyver):
        try:
            sh("python%s -c 'import %s'" % (pyver, modname),
               stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            return False
        else:
            return True

    def sh(cmd, stdout=None, stderr=None):
        subprocess.check_call(cmd, shell=True, stdout=stdout, stderr=stderr)

    def pip_install(modname, pyver):
        if not can_import(modname, pyver) :
            section("installing %s for python%s" % (modname, pyver))
            if which("pip%s" % pyver):
                if IS_ROOT:
                    sh("pip%s install %--upgrade s" % (pyver, modname))
                else:
                    sh("pip%s install --user --upgrade %s" % (pyver, modname))
            else:
                if IS_ROOT:
                    sh("python%s -m pip install --upgrade %s" % (pyver, modname))
                else:
                    sh("python%s -m pip install --user --upgrade %s" % (pyver, modname))
        else:
            section("%s already installed for python%s" % (modname, pyver))

    if not os.path.exists("/tmp/get-pip.py"):
        section("downloading pip")
        wget("https://raw.github.com/pypa/pip/master/contrib/get-pip.py", "/tmp/get-pip.py")
    for pyver in VERSIONS:
        if which("python%s" % pyver):
            banner("processing python%s" % pyver)
            verpair = [int(x) for x in pyver.split('.')]
            # install pip
            if not can_import("pip", pyver):
                section("installing pip for python%s" % pyver)
                cmd = "python%s /tmp/get-pip.py" % pyver
                if not IS_ROOT:
                    cmd += "sudo " + cmd
                sh(cmd)
            else:
                section("pip already installed")
            # install ipdb
            if pyver not in ("2.6", "3.2"):
                pip_install("ipdb", pyver)
            # install unittest2
            if pyver == "2.6":
                pip_install("unittest2", pyver)
            # install others
            pip_install("nose", pyver)
            pip_install("pyflakes", pyver)
            pip_install("flake8", pyver)  # also installs pep8

    # autocompletion
    if not os.path.exists(os.path.expanduser("~/.pythonstart")):
        section("getting ~/.pythonstart")
        wget("http://code.activestate.com/recipes/578098/download/1/",
             "~/.pythonstart")
    if not "PYTHONSTARTUP" in os.environ:
        section("ERR: PYTHONSTARTUP is not set")
END
}


# upgrades all python libs
function sh-py-pip-upgrade-all() {
    pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U --user
}


# paste file on a pastebin-like service and return the generated url
function sh-pastebin() {
    file=$1 python << END
if 1:
    import urllib, urllib2, os, sys
    file = os.environ['file']
    try:
        file = os.environ['file']
        assert file
    except (KeyError, AssertionError):
        sys.exit('usage: pastebin <fname>')
    code = open(file, 'rb').read()
    lang = 'Python' if file.endswith('.py') else 'Plain+Text'
    data = urllib.urlencode(dict(lang='Python', code=code, run=True, submit='Submit'))
    req = urllib2.Request('http://codepad.org/', data)
    f = urllib2.urlopen(req)
    assert f.getcode() == 200, f.getcode()
    print f.geturl()
END
}

# =============================================================================
# Network
# =============================================================================

# ...in case wget/curl are missing
# usage: sh-httpfetch <url> [<file>]
function sh-httpfetch() {
    url=$1 dest=$2 python << END
from __future__ import print_function
if 1:
    import os, urllib2, sys
    url = os.environ['url']
    dest = os.environ['dest']
    if not url:
        sys.exit('usage: sh-httpfetch <url> [<file>]')
    print("getting %s to %s" % (url, dest), file=sys.stderr)
    if not '://' in url:
        url = 'http://' + url
    # try to disable cache
    req = urllib2.Request(url)
    req.add_header('Cache-Control', 'max-age=0')
    req.add_header('Pragma', 'no-cache')
    url = urllib2.urlopen(req)
    data = url.read()
    if dest:
        f = open(dest, 'w')
    else:
        f = sys.stdout
    with f:
        f.write(data)
END
}

# add your public SSH key to a remote host
function sh-ssh-add-remote-keys() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "usage: ssh-add-remote-keys <user> <remote-ip> "
        return
    fi
    cat ~/.ssh/id_rsa.pub | ssh $1@$2 "cat - >> ~/.ssh/authorized_keys"
    echo "done"
}

# show public ip
function sh-myip() {
    sh-httpfetch icanhazip.com
}


# =============================================================================
# System
# =============================================================================

# install package
function sh-install() {
    if [ -z "$1" ]; then
        echo "usage: sh-install <pkg-name> "
        return
    fi
    # TODO: better handling of auth (sudo)
    # ubuntu / debian
    if type -P apt > /dev/null; then
        sudo apt-get install $1
    # osx
    elif type -P brew > /dev/null; then
        sudo brew install $1
    # freebsd
    elif type -P pkg > /dev/null; then
        pkg install $1
    # freebsd
    elif type -P pkg_add > /dev/null; then
        pkg_add -r $1
    else
        echo "system not supported"
    fi
}

# remove package
function sh-uninstall() {
    if [ -z "$1" ]; then
        echo "usage: sh-uninstall <pkg-name> "
        return
    fi

    # TODO: better handling of auth (sudo)
    # ubuntu / debian
    if type -P apt > /dev/null; then
        sudo apt-get remove $1
    # osx
    elif type -P brew > /dev/null; then
        sudo brew uninstall $1
    # freebsd
    elif type -P pkg_delete > /dev/null; then
        pkg_delete $1
    else
        echo "system not supported"
    fi
}

# shows apt history
if type -P vim > /dev/null; then
    function sh-apt-history() {
        case "$1" in
            install)
                cat /var/log/dpkg.log | grep 'install '
                ;;
            upgrade|remove)
                cat /var/log/dpkg.log | grep $1
                ;;
            rollback)
                cat /var/log/dpkg.log | grep upgrade | \
                    grep "$2" -A10000000 | \
                    grep "$3" -B10000000 | \
                    awk '{print $4"="$5}'
                ;;
            *)
                echo "usage: apt-history [install|upgrade|remove|rollback]"
                ;;
        esac
    }
fi

# turn off keyboard backlight
if [ `hostname` = $_LAPTOP ]; then
    function sh-keyboard-turnoff-backlight() {
        echo 0 | sudo tee /sys/class/leds/asus::kbd_backlight/brightness > /dev/null
    }
    sh-keyboard-turnoff-backlight
fi

# =============================================================================
# Files
# =============================================================================

# clean unnecessary files
function sh-clean-buid-files() {
    $(which rm) -f `find . -type f -name \*.py[co]`
    $(which rm) -f `find . -type f -name \*.so`
    $(which rm) -f `find . -type f -name .\*~`
    $(which rm) -f `find . -type f -name \*.orig`
    $(which rm) -f `find . -type f -name \*.bak`
    $(which rm) -f `find . -type f -name \*.rej`
    $(which rm) -rf `find . -type d -name __pycache__`
    $(which rm) -rf *.egg-info
    #$(which rm) -rf build
    #$(which rm) -rf dist
    #$(which rm) -rf docs/_build
}

# extract all archives just by typing 'extract arch.ext'
function sh-extract-archive() {
    if [ -f $1 ] ; then
        case $1 in
            *.tar.bz2)   tar xvjf $1;;
            *.tar.gz)    tar xvzf $1;;
            *.bz2)       bunzip2 $1;;
            *.rar)       unrar x $1;;
            *.gz)        gunzip $1;;
            *.tar)       tar xvf $1;;
            *.tbz2)      tar xvjf $1;;
            *.tgz)       tar xvzf $1;;
            *.tar.zx)    tar xvfJ $1;;
            *.zip)       unzip $1;;
            *.Z)         uncompress $1;;
            *.7z)        7z x $1;;
            *)           echo "don't know how to extract '$1'" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# creates an archive from given directory
function sh-mktgz() { tar cvzf "${1%%/}.tar.gz"  "${1%%/}/"; }
function sh-mkbz2() { tar cvjf "${1%%/}.tar.bz2" "${1%%/}/"; }

# ===========================================================================
# Others
# ===========================================================================

function sh-terminal-git() {
    if [[ $OSTYPE == *linux-gnu* ]]; then
        if [ "$PS1" ]; then
            if [ "$BASH" ]; then
                PS1='\w\[\e[m\]$(__git_ps1 " \[\e[0;32m\]{%s}\[\e[m\]")\[\e[0;31m\]$\[\e[m\] '
                return
            fi
        fi
    fi
    sh-terminal-default
}

function sh-terminal-default() {
    if [ `hostname` = $_LAPTOP ]; then
        :
        PS1='\[\033[01;0m\]\w\$ '
        #PS1='\[\033[01;30m\]\u\[\033[01;30m\]@\[\033[01;31m\]\h\[\033[00;34m\]:\[\033[01;35m\]\w\[\033[00;34m\]\[\033[01;30m\]$\[\033[00m\] '
    else
        PS1='\u@\[\033[01;31m\]\h\[\033[01;0m\]\w\$ '
    fi
}

# =============================================================================
# end of custom functions
# =============================================================================

# pip bash completion start
function _pip_completion() {
    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   PIP_AUTO_COMPLETE=1 $1 ) )
}
complete -o default -F _pip_completion pip

# SSH remote completion XXX / TODO: test this
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi
if [ -f ~/.ssh/known_hosts ]; then
    SSH_COMPLETE=( $(cat ~/.ssh/known_hosts | \
    cut -f 1 -d ' ' | \
    sed -e s/,.*//g | \
    uniq | \
    egrep -v [0123456789]) )
    complete -o default -W "${SSH_COMPLETE[*]}" ssh
fi

# completion for sudo
complete -cf sudo

# webcam (notebook only)
if [ `hostname` = $_LAPTOP ]; then
    v4lctl bright 100%
fi

# terminal prefix + welcome message
# _black='\e[0;30m'
# _blue='\e[0;34m'
# _green='\e[0;32m'
# _cyan='\e[0;36m'
# _red='\e[0;31m'
# _purple='\e[0;35m'
_brown='\e[0;33m'
# _lightgray='\e[0;37m'
# _darkgray='\e[1;30m'
# _lightblue='\e[1;34m'
# _lightgreen='\e[1;32m'
# _lightcyan='\e[1;36m'
# _lightred='\e[1;31m'
# _lightpurple='\e[1;35m'
# _yellow='\e[1;33m'
# _white='\e[1;37m'
_nc='\e[0m'

function _print_sysinfo() {
    echo -en "${_brown}"
    echo -e "${_brown}Hostname: `hostname`"
    echo -e "Date:     `date +"%Y-%m-%d %H:%M:%S"`"
    echo -e "Kernel:   `uname -s` `uname -r`"
    #echo -e "System:   $OSTYPE"
    if [ `uname -m` == 'x86_64' ]; then
        echo -e "Arch:     64-bit"
    else
        echo -e "Arch:     32-bit"
    fi
    echo -e "Python:   `python -c 'import sys; sys.stdout.write(sys.version.split()[0])'`"
#    echo -e "================================================================="
    echo -en "${_nc}"
}

_print_sysinfo

if [ -d .git ]; then
    sh-terminal-git
else
    sh-terminal-default
fi
