#!/usr/bin/env bash

# ===========================================================================
# Constants
# ===========================================================================

PLATFORM="$(python -c "import sys; print(sys.platform)")"
SYSCONF_BIN_DIR="$(python -c "import sysconf; print(sysconf.DIR_BIN)")"
PIP_URL="https://bootstrap.pypa.io/get-pip.py"
LAPTOP="N501VW"  # mt hostname / laptop id
HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"  # this dir


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

# set English (instead of Italian) for commands output
#export LANG=en_US.UTF-8

# http://stackoverflow.com/a/5130969/376587
# "ls | c" copies the output, "v" paste it in the terminal
if [[ $PLATFORM == *linux* ]]; then
    alias "c=xclip"
    alias "cc=xclip -selection clipboard"  # copy to GUI
    alias "v=xclip -o"
fi

# ===========================================================================
# Custom settings
# ===========================================================================

# ~/bin is now in the list of exec dirs
PATH="$HOME/bin:$PATH"

# Add sysconf bin dir to PATH.
PATH=$PATH:$SYSCONF_BIN_DIR

# Webcam brightness (notebook only)
# TODO: this is slow; may want to run this in a subprocess (nohup?)
# or move it elsewhere.
if [ `hostname` = $LAPTOP ]; then
    v4lctl bright 100%
fi

# don't use ^D to exit
set -o ignoreeof

# set paginator
export PAGER="less"

# save the history of multiple shells in a single file, see:
# http://unix.stackexchange.com/questions/1288
export HISTCONTROL=ignoredups:erasedups  # no duplicate entries
export HISTSIZE=100000                   # big big history
export HISTFILESIZE=100000               # big big history
shopt -s histappend                # append to history, don't overwrite it
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

# pip bash completion start
_pip_completion() {
    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   PIP_AUTO_COMPLETE=1 $1 ) )
}
complete -o default -F _pip_completion pip

# bash completion
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi

# SSH completion (TODO: test this)
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

# thefuck
if type -P thefuck > /dev/null; then
    eval $(thefuck --alias)
fi

# ===========================================================================
# Aliases
# ===========================================================================

# ls (also see: http://www.noah.org/engineering/dotfiles/.bashrc)
if [[ $PLATFORM == *linux* ]]; then
    alias ls='ls -hF --color --group-directories-first --time-style=+"%Y-%m-%d %H:%M"'
else
    export CLICOLOR=1
    alias ls='ls -hF'
fi
alias l='ls'
alias ll='ls -la'
alias ls-ext='ls -lXB'        # sort by extension
alias ls-biggest='BLOCKSIZE=1048576; du -x | sort -nr | head -20 | grep -v \.hg | grep -v \.git '
alias ls-size='ls -lSr'        # sort by size
alias ls-hidden='ls -a'        # show hidden files
alias ls-date='ls -ltr'        # sort by date
alias ls-tree='tree -Cs'        # nice alternative to 'ls'
alias ls-dirs='ls -l | grep "^d"'   #list only directories
alias ls-files='ls -l | grep -v "^d"'   #list only file

# cd - automatically do an ls after each cd
cd() {
    if [ -n "$1" ]; then
        builtin cd "$@" && ls
    else
        builtin cd ~ && ls
    fi

    # if I'm in a GIT directory, make it look cool
    if [ -d .git ]; then
        _sh_term_git
    else
        _sh_term_default
    fi
}
alias ..='cd ..'
alias cd..='cd ..'

# git
alias g='git'
alias git-ci-push='git ci -a -m "progress" && git push'
alias git-pull='git pull -u -v'

# mercurial
alias hg-ci-push='hg ci -m "progress" && hg push'
alias hg-pull='hg pull -u -v'

# sublime
alias s='subl'

# vim
if type -P vim > /dev/null; then
    export EDITOR="vim"
    export VISUAL="vim"
    alias vi="vim"
else
    export EDITOR="vi"
    export VISUAL="vi"
fi

# grep (and variants)
if [[ $PLATFORM == *linux* ]]; then
    alias grep='grep --color=auto --exclude=*.pyc --exclude=*.orig --exclude=*.rej --exclude-dir=.svn --exclude-dir=.egg-info --exclude-dir=.hg --exclude-dir=.git'
fi
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

# df
alias df='df -h'
alias du='du -h -c'

# map reload to source (original reload is a trap)
alias reload='source ~/.bashrc'

# wget - overwrite by default, don't check SSL cert
alias wget='wget -N --no-check-certificate'

# ssh - don't propt "are you sure...(y|n)?"
alias ssh='ssh -o StrictHostKeyChecking=no'

# substitute for 'realpath' cmd, which is not always available
realpath() {
    if [ -z "$1" ] ; then
        echo "usage: realpath <path>"
        return
    fi
    python -c "import os; print(os.path.realpath(os.path.normpath('$1')))"
}

# =============================================================================
# User defined utility functions start here.
# All starts with "sh-" namespace so that I won't pollute PATH namespace.
# =============================================================================


# =============================================================================
# Dev / Python
# =============================================================================

# try to find a virtualenv and activate it
sh-py-source-venv() {
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

# clean unnecessary files
sh-py-clean-build-files() {
    $(which rm) -f `find . -type f -name \*.py[co]`
    $(which rm) -f `find . -type f -name \*.so`
    $(which rm) -f `find . -type f -name .\*~`
    $(which rm) -f `find . -type f -name \*.orig`
    $(which rm) -f `find . -type f -name \*.bak`
    $(which rm) -f `find . -type f -name \*.rej`
    $(which rm) -rf `find . -type d -name __pycache__`
    $(which rm) -rf *.egg-info
    if [ -f setup.py ]; then
        $(which rm) -rf build
        $(which rm) -rf dist
    fi
}

# install python for the given python version
sh-py-install-pip() {
    if [ -z "$1" ] ; then
        echo "usage: py-install-pip <python>"
        return
    fi

    # python 2.4 and 2.5
    if [ $1 = "python2.4" ] || [ $1 = "python2.5" ]; then
        sh-net-httpfetch https://bitbucket.org/pypa/setuptools/raw/bootstrap-py24/ez_setup.py > /tmp/ez_setup.py
        $1 /tmp/ez_setup.py
        if [ $1 = "python2.4" ]; then
            easy_install-2.4 pip==1.1
        else
            easy_install-2.5 pip==1.1
        fi
    # python 2.6+
    else
        sh-net-httpfetch $PIP_URL > /tmp/get-pip.py
        if [ "$(id -u)" == "0" ]; then
            $1 /tmp/get-pip.py
        else
            sudo $1 /tmp/get-pip.py
        fi
    fi
}

# print all python module imports
sh-py-find-imports() {
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
sh-py-setup-all() {
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
END
}


# upgrades all python libs
sh-py-pip-upgrade-all() {
    pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U --user
}


# =============================================================================
# Network
# =============================================================================

alias sh-net-netstat-listen='sudo netstat -antp | grep LISTEN'
alias sh-net-ping-google='ping google.com'

# ...in case wget/curl are missing
# usage: sh-net-httpfetch <url> [<file>]
sh-net-httpfetch() {
    url=$1 dest=$2 python << END
from __future__ import print_function
if 1:
    import os, urllib2, sys
    url = os.environ['url']
    dest = os.environ['dest']
    if not url:
        sys.exit('usage: sh-net-httpfetch <url> [<file>]')
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

# paste file on a pastebin-like service and return the generated url
sh-net-pastebin() {
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
    url = f.geturl()
    if 'DISPLAY' in os.environ:
        os.system('google-chrome %s' % url)
END
}


# show public ip
sh-net-myip() {
    sh-net-httpfetch icanhazip.com
}


# add your public SSH key to a remote host
sh-net-scp-ssh-keys() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "usage: ssh-add-remote-keys <user> <remote-ip> "
        return
    fi
    cat ~/.ssh/id_rsa.pub | ssh $1@$2 "cat - >> ~/.ssh/authorized_keys"
    echo "done"
}


# =============================================================================
# Packages
# =============================================================================

# install package
sh-pkg-install() {
    if [ -z "$1" ]; then
        echo "usage: sh-pkg-install <pkg-name> "
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
sh-pkg-uninstall() {
    if [ -z "$1" ]; then
        echo "usage: sh-pkg-uninstall <pkg-name> "
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
    elif type -P pkg > /dev/null; then
        pkg remove $1
    # freebsd
    elif type -P pkg_delete > /dev/null; then
        pkg_delete $1
    else
        echo "system not supported"
    fi
}

# search package
sh-pkg-search() {
    if [ -z "$1" ]; then
        echo "usage: sh-pkg-search <pkg-name> "
        return
    fi
    # TODO: better handling of auth (sudo)
    # ubuntu / debian
    if type -P apt > /dev/null; then
        sudo apt-cache search $1
    # osx
    elif type -P brew > /dev/null; then
        echo TODO
    # freebsd
    elif type -P pkg > /dev/null; then
        echo TODO
    # freebsd
    elif type -P pkg_add > /dev/null; then
        echo TODO
    else
        echo "system not supported"
    fi
}


# search package
sh-pkg-list-installed() {
    # ubuntu / debian
    if type -P dpkg > /dev/null; then
        sudo dpkg -l
    # osx
    elif type -P brew > /dev/null; then
        echo TODO
    # freebsd
    elif type -P pkg > /dev/null; then
        echo TODO
    # freebsd
    elif type -P pkg_add > /dev/null; then
        echo TODO
    else
        echo "system not supported"
    fi
}


# shows apt history
if type -P dpkg > /dev/null; then
    sh-pkg-history() {
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


# =============================================================================
# Paths
# =============================================================================

# extract all archives just by typing 'extract arch.ext'
sh-path-arch-extract() {
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


# print size path
sh-path-size() {
    if [ -z "$1" ]; then
        echo "usage: sh-path-size <path> "
        return
    fi
    du -hs $1
}


# ===========================================================================
# Internal utils
# ===========================================================================

_sh_term_git() {
    if [[ $OSTYPE == *linux-gnu* ]]; then
        if [ "$PS1" ]; then
            if [ "$BASH" ]; then
                PS1='\w\[\e[m\]$(__git_ps1 " \[\e[0;32m\]{%s}\[\e[m\]")\[\e[0;31m\]$\[\e[m\] '
                return
            fi
        fi
    fi
    _sh_term_default
}

_sh_term_default() {
    if [ `hostname` = $LAPTOP ]; then
        :
        PS1='\[\033[01;0m\]\w\$ '
        #PS1='\[\033[01;30m\]\u\[\033[01;30m\]@\[\033[01;31m\]\h\[\033[00;34m\]:\[\033[01;35m\]\w\[\033[00;34m\]\[\033[01;30m\]$\[\033[00m\] '
    else
        PS1='\u@\[\033[01;31m\]\h\[\033[01;0m\]\w\$ '
    fi
}

_brown='\e[0;33m'
_nc='\e[0m'
# _black='\e[0;30m'
# _blue='\e[0;34m'
# _green='\e[0;32m'
# _cyan='\e[0;36m'
# _red='\e[0;31m'
# _purple='\e[0;35m'
# _lightgray='\e[0;37m'
# _darkgray='\e[1;30m'
# _lightblue='\e[1;34m'
# _lightgreen='\e[1;32m'
# _lightcyan='\e[1;36m'
# _lightred='\e[1;31m'
# _lightpurple='\e[1;35m'
# _yellow='\e[1;33m'
# _white='\e[1;37m'

# Print system info when a new shell is opened
_print_sysinfo() {
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
    echo -en "${_nc}"
}



# =============================================================================
# Final stuff
# =============================================================================

# print a banner to figure out what machine I'm on
_print_sysinfo

# set the right terminal in case I'm in a GIT dir
if [ -d .git ]; then
    _sh_term_git
else
    _sh_term_default
fi
