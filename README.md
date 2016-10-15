Personal ([Giampaolo](http://grodola.blogspot.com/p/about.html)) system config
utilities to install on a brand new UNIX system. This basically does 3 things:

Installation
============

On a brand new system you really want to do:

```
make all
```

This will do the following:

* `make sysinstall`: install all basic system deps (e.g. python, gcc, sudo)
* `make sysconfig`: config system preferences (e.g. add sudoers)
* `make userconfig`: * symnlink user config files to this cloned repository  (e.g.
  [.bashrc](https://github.com/giampaolo/sysconf/blob/master/static/home/.bashrc),
  [.vimrc](https://github.com/giampaolo/sysconf/blob/master/static/home/.vimrc),
  [.gitconfig](https://github.com/giampaolo/sysconf/blob/master/static/home/.gitconfig))
* `make install`: install this package (that means you'll get
   [bin/grep.py](https://github.com/giampaolo/sysconf/blob/master/bin/grep.py),
   [bin/killall.py](https://github.com/giampaolo/sysconf/blob/master/bin/killall.py),
   and other scritps in [bin](https://github.com/giampaolo/sysconf/blob/master/bin/) directory.

**WARNING**: these are my personal system settings; your tastes may differ so
be aware!

Interesting stand-alone parts which may be useful
=================================================

* [home/.bashrc](https://github.com/giampaolo/sysconf/blob/master/static/home/.bashrc)
* [home/.vimrc](https://github.com/giampaolo/sysconf/blob/master/static/home/.vimrc)
* [home/.pythonstart](https://github.com/giampaolo/sysconf/blob/master/static/home/.pythonstart): auto-completion for the interatctive interpreter
* [bin/grep.py](https://github.com/giampaolo/sysconf/blob/master/bin/grep.py):
  a clone of "ack" command but simpler.
* [bin/codestats.py](https://github.com/giampaolo/sysconf/blob/master/bin/codestats.py):
  show code stats about a project.
* [bin/killall.py](https://github.com/giampaolo/sysconf/blob/master/bin/killall.py):
  a clone of "killall" command but it tries harder to kill a process.
* [bin/find_broken_links.py](https://github.com/giampaolo/sysconf/blob/master/bin/find_broken_links.py):
  find broken links in text files
