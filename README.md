Personal ([Giampaolo Rodola'](http://grodola.blogspot.com/p/about.html))
system config utilities to install on a brand new UNIX system.
This is my attempt to write a single set of scripts to make my UNIX experience
the same across different UNIX flavors.

Installation
============

On a brand new system you really want to do:

```bash
make all
```

This will do the following:

* `make sysinstall`: install all basic system deps (e.g. python, gcc, sudo)
* `make sysconfig`: config system preferences (e.g. add user to sudoers)
* `make userconfig`: symlinks user config files to this cloned repository  (e.g.
  [.bashrc](https://github.com/giampaolo/sysconf/blob/master/home/.bashrc),
  [.vimrc](https://github.com/giampaolo/sysconf/blob/master/home/.vimrc),
  [.gitconfig](https://github.com/giampaolo/sysconf/blob/master/home/.gitconfig)
  and others).
* `make install`: install this package (that means you'll get
   [bin/grep.py](https://github.com/giampaolo/sysconf/blob/master/bin/grep.py),
   [bin/killall.py](https://github.com/giampaolo/sysconf/blob/master/bin/killall.py),
   and other scritps in [bin](https://github.com/giampaolo/sysconf/blob/master/bin/) directory.

If GIT is not installed and you can't clone this repo do:

```bash
wget https://github.com/giampaolo/sysconf/tarball/master && tar zxvf master
eval $(ssh-agent)  # do not prompt password on GIT push
```

**WARNING**: these are my personal system settings; your tastes may differ so
be aware!

Interesting stand-alone parts which may be useful
=================================================

* [home/.bashrc](https://github.com/giampaolo/sysconf/blob/master/home/.bashrc)
* [home/.vimrc](https://github.com/giampaolo/sysconf/blob/master/home/.vimrc)
* [home/.pythonstart](https://github.com/giampaolo/sysconf/blob/master/home/.pythonstart): auto-completion for the interatctive interpreter
* [bin/grep.py](https://github.com/giampaolo/sysconf/blob/master/bin/grep.py):
  a clone of "ack" command but simpler.
* [bin/codestats.py](https://github.com/giampaolo/sysconf/blob/master/bin/codestats.py):
  show code stats about a project.
* [bin/killall.py](https://github.com/giampaolo/sysconf/blob/master/bin/killall.py):
  a clone of "killall" command but it tries harder to kill a process.
* [bin/find_broken_links.py](https://github.com/giampaolo/sysconf/blob/master/bin/find_broken_links.py):
  find broken links in text files
