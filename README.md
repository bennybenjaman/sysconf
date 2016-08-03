Personal ([Giampaolo](http://grodola.blogspot.com/p/about.html)) system config
utilities to install on a brand new UNIX system. This basically does 3 things:

* install systems deps (python-dev, gcc, sudo, etc.) on different UNIX flavors
  (Linux, BSD, OSX, Solaris)
* configure system files (e.g. add user to sudoers)
* symnlink user config files to this cloned repository (e.g. [.bashrc](https://github.com/giampaolo/sysconf/blob/master/static/home/.bashrc), [.vimrc](https://github.com/giampaolo/sysconf/blob/master/static/home/.vimrc), [.gitconfig](https://github.com/giampaolo/sysconf/blob/master/static/home/.gitconfig))

Pre installation
================

**FreeBSD**

```
pkg install python bash git
```

**If GIT is not installed**

```
wget https://github.com/giampaolo/sysconf/tarball/master && tar zxvf master
eval $(ssh-agent)  # do not prompt password on GIT push
```

**Solaris**

```
pkg install python git gcc
```


Installation
============

```
git clone git@github.com:giampaolo/sysconf.git
cd sysconfig
make install
```

Then run one of the following commands:

```
make sysinstall     # install system deps (requires root)
make sysconfig      # config system files (requires root)
make userconfig     # config user files
make runall         # do the 3 above
```

**WARNING**: these are my personal system settings; your tastes may differ so
be aware!

Interesting stand-alone parts which may be useful
=================================================

* [home/.bashrc](https://github.com/giampaolo/sysconf/blob/master/static/home/.bashrc)
* [home/.vimrc](https://github.com/giampaolo/sysconf/blob/master/static/home/.vimrc)
* [home/.pythonstart](https://github.com/giampaolo/sysconf/blob/master/static/home/.pythonstart): auto-completion for the interatctive interpreter
* [bin/grep.py](https://github.com/giampaolo/sysconf/blob/master/bin/grep.py):
  a clone of "ack" command but simpler.
* [bin/killall.py](https://github.com/giampaolo/sysconf/blob/master/bin/killall.py):
  a clone of "killall" command but it tries harder to kill a process.
