
PACKAGE_NAME=termprop
PYTHON=python

.PHONY: smoketest clean install uninstall

build: update_license_block smoketest
	$(PYTHON) setup.py sdist
	python2.5 setup.py bdist_egg
	python2.6 setup.py bdist_egg
	python2.7 setup.py bdist_egg

update_license_block:
	chmod +x update_license
	find . -type f | grep '\(.py\|.c\)$$' | xargs ./update_license

install: smoketest
	$(PYTHON) -c "import setuptools" || curl http://peak.telecommunity.com/dist/ez_setup.py | python
	$(PYTHON) setup.py install

uninstall:
	yes | pip uninstall $(PACKAGE_NAME)

clean:
	rm -rf dist/ build/ *.egg-info *.pyc **/*.pyc

smoketest:
	$(PYTHON) setup.py test

update: clean smoketest
	$(PYTHON) setup.py register
	$(PYTHON) setup.py sdist upload
	python2.6 setup.py bdist_egg upload
	python2.7 setup.py bdist_egg upload

