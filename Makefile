# Shortcuts for various tasks (UNIX only).
# To use a specific Python version run: "make install PYTHON=python3.3"

# You can set these variables from the command line.
PYTHON = python
INSTALL_OPTS = `$(PYTHON) -c "import os; print('' if os.geteuid() == 0 else '--user')"`

clean:
	rm -f `find . -type f -name \*.py[co]`
	rm -f `find . -type f -name \*.so`
	rm -f `find . -type f -name \*.~`
	rm -f `find . -type f -name \*.orig`
	rm -f `find . -type f -name \*.bak`
	rm -f `find . -type f -name \*.rej`
	rm -rf `find . -type d -name __pycache__`
	rm -rf *.core
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf build
	rm -rf dist


# Install pip (only if necessary).
install-pip:
	$(PYTHON) -c "import sys, ssl, os, pkgutil, tempfile, atexit; \
				pyexc = 'from urllib.request import urlopen' if sys.version_info[0] == 3 else 'from urllib2 import urlopen'; \
				exec(pyexc); \
				context = ssl._create_unverified_context() if hasattr(ssl, '_create_unverified_context') else None; \
				kw = dict(context=context) if context else {}; \
				req = urlopen('https://bootstrap.pypa.io/get-pip.py', **kw); \
				data = req.read(); \
				f = tempfile.NamedTemporaryFile(suffix='.py'); \
				atexit.register(f.close); \
				f.write(data); \
				f.flush(); \
				print('downloaded %s' % f.name); \
				code = os.system('%s %s' % (sys.executable, f.name)); \
				sys.exit(code);"

# install this pkg
install:
	$(PYTHON) -m pip install $(INSTALL_OPTS) --upgrade setuptools docopt futures
	$(PYTHON) setup.py develop $(INSTALL_OPTS)

# install base system deps (python, gcc, sudo, etc.)
sysinstall:
	./scripts/sysinstall

# configure system (e.g. add sudoers)
sysconfig:
	./scripts/sysconfig

# configure user deps (e.g. add bashrc)
userconfig:
	./scripts/userconfig

all:
	$(MAKE) sysinstall
	$(MAKE) sysconfig
	$(MAKE) install
	$(MAKE) userconfig

flake8:
	@git ls-files | grep \\.py$ | xargs $(PYTHON) -m flake8

autopep8:
	git ls-files | grep \\.py$ | xargs $(PYTHON) -m autopep8 --aggressive --in-place --experimental
	$(PYTHON) -m autopep8 --aggressive --in-place scripts/userconfig --experimental
