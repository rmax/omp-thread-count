#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import subprocess
import sys

from setuptools import setup
from setuptools.command import build_ext as _build_ext
from setuptools.extension import Extension


PKGNAME = "omp_thread_count"


class build_ext(_build_ext.build_ext):

    def assert_openmp_support(self):
        name = self.compiler.compiler[0]  # command list
        ret = subprocess.call(['scripts/check_for_openmp.py', '-c', name])
        if ret != 0:
            sys.stderr.write("Compiler check failed. "
                             "Run scripts/check_for_openmp.py -v\n")
            sys.exit(ret)

    def finalize_options(self):
        # Cythonize on build_ext only.
        from Cython.Build import cythonize
        self.distribution.ext_modules[:] = cythonize(
            self.distribution.ext_modules,
            compiler_directives={'embedsignature': True},
        )
        _build_ext.build_ext.finalize_options(self)

    def build_extensions(self):
        self.assert_openmp_support()
        _build_ext.build_ext.build_extensions(self)


def get_extensions():
    kwargs = {
        'include_dirs': ['src/%s/include/' % PKGNAME],
        'extra_compile_args': ['-fopenmp'],
        'extra_link_args': ['-fopenmp'],
    }
    return [
        Extension('%s._omp' % PKGNAME, ['src/%s/_omp.pyx' % PKGNAME], **kwargs)
    ]


def read_text(filename):
    with io.open(filename) as fp:
        return fp.read()


short_description = (
    "A small utility to get the actual number of threads "
    "used by OpenMP via Cython bindings."
)
long_description = "\n\n".join([
    read_text('README.rst'),
    read_text('HISTORY.rst'),
])

setup(
    name='omp-thread-count',
    version='0.2.0',
    description=short_description,
    long_description=long_description,
    author="Rolando Espinoza",
    author_email='rolando at rmax.io',
    url='https://github.com/rolando/omp-thread-count',
    packages=[PKGNAME],
    package_data={
        PKGNAME: ['*.pyx', '*.pxd', 'include/*.h'],
    },
    package_dir={'': 'src'},
    license="MIT",
    zip_safe=False,
    keywords=['openmp', 'threads'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    cmdclass={'build_ext': build_ext},
    ext_modules=get_extensions(),
    setup_requires=['cython>=0.24'],
)
