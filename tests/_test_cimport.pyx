"""Test cimporting the function directly.
from omp_thread_count._omp cimport get_thread_count as _get_thread_count


def get_thread_count():
    return _get_thread_count()
