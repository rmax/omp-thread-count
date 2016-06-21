"""Test cimporting the function directly."""
from omp_thread_count._omp cimport get_thread_count as c_get_thread_count


def get_thread_count():
    return c_get_thread_count()
