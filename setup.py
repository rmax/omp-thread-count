#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys

from setuptools import setup
from setuptools.command import build_ext as _build_ext
from setuptools.extension import Extension


USE_CYTHON = bool(os.environ.get('USE_CYTHON'))


class build_ext(_build_ext.build_ext):

    def assert_openmp_support(self):
        name = self.compiler.compiler[0]  # command list
        ret = subprocess.call(['scripts/check_for_openmp.py', '-c', name])
        if ret != 0:
            sys.stderr.write("Compiler check failed. Run scripts/check_for_openmp.py -v\n")
            sys.exit(ret)

    def build_extensions(self):
        self.assert_openmp_support()
        _build_ext.build_ext.build_extensions(self)


def get_extensions(use_cython=USE_CYTHON):
    module = 'omp_thread_count'
    ext = '.pyx' if USE_CYTHON else '.c'
    sources = ['src/omp_thread_count' + ext]
    extensions = [
        Extension(module, sources,
                  include_dirs=['src'],
                  extra_compile_args=['-fopenmp'],
                  extra_link_args=['-fopenmp']),
    ]
    if USE_CYTHON:
        from Cython.Build import cythonize
        extensions = cythonize(extensions)
    return extensions


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


setup(
    name='omp-thread-count',
    version='0.1.0',
    description="A small utility to get the actual number of threads used by OMP via Cython.",
    long_description=readme + '\n\n' + history,
    author="Rolando Espinoza",
    author_email='rolando at rmax.io',
    url='https://github.com/rolando/omp-thread-count',
    license="MIT",
    ext_modules=get_extensions(),
    zip_safe=False,
    keywords=['openmp', 'threads', 'counter'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    cmdclass={'build_ext': build_ext},
)
