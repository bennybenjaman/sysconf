# Shortcuts for various tasks (UNIX only).
# To use a specific Python version run: "make install PYTHON=python3.3"

# You can set these variables from the command line.
PYTHON = python

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

install:
	# Install pip (only if necessary).
	$(PYTHON) -c "import sys, ssl, os, pkgutil, tempfile, atexit; \
				sys.exit(0) if pkgutil.find_loader('pip') else None; \
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
				code = os.system('%s %s --user' % (sys.executable, f.name)); \
				sys.exit(code);"
	# Install setuptools (required 'cause we want 'develop' / 'edit' mode).
	$(PYTHON) -m pip install --user --upgrade setuptools docopt futures
	# Finally install this pkg.
	$(PYTHON) setup.py develop --user

runall:
	$(PYTHON) setup.py runall

sysinstall:
	sh scripts/sysinstall

sysconfig:
	$(PYTHON) setup.py sysconfig

userconfig:
	$(PYTHON) setup.py userconfig

flake8:
	@git ls-files | grep \\.py$ | xargs $(PYTHON) -m flake8

autopep8:
	git ls-files | grep \\.py$ | xargs $(PYTHON) -m autopep8 --aggressive --in-place --experimental
	$(PYTHON) -m autopep8 --aggressive --in-place scripts/userconfig --experimental
