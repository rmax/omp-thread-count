=====================
OpenMP Thread Counter
=====================

.. image:: https://img.shields.io/pypi/v/omp-thread-count.svg
        :target: https://pypi.python.org/pypi/omp-thread-count

.. image:: https://img.shields.io/travis/rolando/omp-thread-count.svg
        :target: https://travis-ci.org/rolando/omp-thread-count

.. image:: https://readthedocs.org/projects/omp-thread-count/badge/?version=latest
        :target: https://readthedocs.org/projects/omp-thread-count/?badge=latest
        :alt: Documentation Status


A small Python module to get the actual number of threads used by OMP via Cython bindings.

* Free software: MIT license
* Documentation: https://omp-thread-count.readthedocs.org.

Why
---

Because GCC/Cython always returned 1 when calling ``openmp.get_thread_num`` or ``openmp.get_max_threads``.

Installation
------------

To install run::

  pip install omp-thread-count

In OSX, and possibly other platforms, you may need to specify a compiler with
OpenMP support, like this::

  CC=gcc-4.8 pip install omp-thread-count

Usage
-----

Importing from python code:

.. code:: python
 
  import omp_thread_count

  n_threads = omp_thread_count.get_thread_count()


Importing from cython code:

.. code:: python

  from omp_thread_count._omp cimport get_thread_count

Use ``omp_thread_count.get_includes()`` in your extensions' ``include_dirs`` to
use the header files.


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
