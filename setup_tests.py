#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup
from setuptools.extension import Extension

from Cython.Build import cythonize

import omp_thread_count


def get_extensions():
    kwargs = {
        'include_dirs': omp_thread_count.get_includes(),
        'extra_compile_args': ['-fopenmp'],
        'extra_link_args': ['-fopenmp'],
    }
    extensions = [
        Extension('tests.*', ['tests/*.pyx'], **kwargs),
    ]
    return cythonize(extensions,
                     compiler_directives={'embedsignature': True})


setup(
    name='omp-thread-count-tests',
    version='0.1.0',
    packages=['tests'],
    package_data={
        "tests": ['*.pyx', '*.pxd'],
    },
    ext_modules=get_extensions(),
)
