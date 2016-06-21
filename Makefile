.PHONY: clean-so clean-test clean-pyc clean-build docs clean
.PHONY: check check-manifest check-setup lint
.PHONY: test test-all coverage
.PHONY: compile-reqs install-reqs
.PHONY: release dist install
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@echo "check - check setup, code style, setup, etc"
	@echo "check-manifest - check manifest"
	@echo "check-setup - check setup"
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "clean-so - remove compiled extensions"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "compile-reqs - compile requirements"
	@echo "install-reqs - install requirements"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "develop - install package in develop mode"
	@echo "install - install the package to the active Python's site-packages"

check: check-setup check-manifest lint

check-setup:
	python setup.py check --strict --metadata --restructuredtext

check-manifest:
	check-manifest

clean: clean-build clean-pyc clean-test clean-cython

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

clean-cython:
	# cleanup generated files
	find . -name '*.c' -exec rm -f {} +
	find . -name '*.so' -exec rm -f {} +

lint:
	flake8 src tests

develop: clean
	python setup.py develop
	python setup_tests.py build_ext --inplace

test: develop
	py.test -v

test-all: clean
	tox -v

coverage: develop
	coverage run --source omp_thread_count -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

compile-reqs:
	pip-compile -v dev-requirements.in -o dev-requirements.txt

install-reqs:
	pip install -r dev-requirements.txt

docs:
	rm -f docs/omp_thread_count.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/omp_thread_count
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist
	# Only upload source files.
	twine upload dist/*.tar.gz

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install
