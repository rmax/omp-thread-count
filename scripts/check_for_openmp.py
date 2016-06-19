#!/usr/bin/env python
from __future__ import unicode_literals

import contextlib
import io
import logging
import os
import shutil
import subprocess
import sys
import tempfile

# see http://openmp.org/wp/openmp-compilers/
OMP_TEST = \
r"""
#include <omp.h>
#include <stdio.h>
int main() {
    #pragma omp parallel
    printf("Hello from thread %d, nthreads %d\n", omp_get_thread_num(), omp_get_num_threads());
    return 0;
}
"""


@contextlib.contextmanager
def chdir(newdir):
    curdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(curdir)


@contextlib.contextmanager
def inside_tmpdir(delete=True):
    tmpdir = tempfile.mkdtemp()
    try:
        with chdir(tmpdir):
            yield tmpdir
    finally:
        if delete:
            shutil.rmtree(tmpdir)


def check_for_openmp(compiler='cc', flags='-Wall -fopenmp',
                     test_filename='test.c', test_output='omp-test',
                     quiet=True, delete=True):
    """Returns 0 if given compiler have support for given flags (-fopenmp by
    default).
    """
    compile_cmd = compiler.split() + flags.split() + [test_filename, '-o', test_output]
    test_cmd = ['./' + test_output]
    with inside_tmpdir(delete=delete) as tmpdir:
        call_kwargs = {}
        if quiet:
            call_kwargs.update({
                'stderr': subprocess.PIPE,
                'stdout': subprocess.PIPE,
            })
        else:
            logging.debug("Workdir: %s", tmpdir)
            call_kwargs.update({
                'stdout': sys.stderr,
            })

        with io.open(test_filename, 'w', encoding='utf8') as fp:
            fp.write(OMP_TEST)

        logging.debug("Compiling %s: %s", test_filename, subprocess.list2cmdline(compile_cmd))
        ret = subprocess.call(compile_cmd, **call_kwargs)
        if ret == 0:
            logging.debug("Running %s", test_output)
            subprocess.check_call(test_cmd, **call_kwargs)
        else:
            logging.error("Failed to compile. Turn -v flag and ensure the compiler "
                          "is installed with OpenMP support.")

    return ret

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--compiler', default=os.environ.get('CC', 'cc'))
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-k', '--keep', action='store_true')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARN)
    sys.exit(check_for_openmp(compiler=args.compiler,
                              quiet=not args.verbose,
                              delete=not args.keep))
