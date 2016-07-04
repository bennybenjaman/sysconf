Personal (Giampaolo) system config utilities to install on a brand new UNIX
system. This basically does 3 things:

* install systems deps (python-dev, gcc, sudo, etc.) on different UNIX flavors
  (Linux, FreeBSD)
* configure system files (e.g. add user to sudoers)
* import user config files (e.g. .vimrc, .gitconfig)

Install it with:

```
git clone git@github.com:giampaolo/sysconfig.git
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

**WARNING**: these are settings to my system setup, so don't try this at home!
