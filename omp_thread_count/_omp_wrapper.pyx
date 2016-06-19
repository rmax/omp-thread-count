# distutils: language = c
from ._omp cimport get_thread_count as _get_thread_count


def get_thread_count():
    """Returns OMP thread count.
    """
    cdef int n
    with nogil:
        n = _get_thread_count()
    return n
