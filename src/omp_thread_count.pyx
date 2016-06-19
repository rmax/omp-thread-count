cdef extern from "omp_thread_count.h":
    int omp_thread_count()


def get_thread_count():
    """get_thread_count()

    Returns OMP thread count.

    """
    return omp_thread_count()
