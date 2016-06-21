# distutils: language = c


cdef extern from "omp_thread_count.h":
    int _omp_thread_count() nogil


cpdef int get_thread_count() nogil:
    """Returns OMP thread count.
    """
    cdef int n
    with nogil:
        n = _omp_thread_count()
    return n
