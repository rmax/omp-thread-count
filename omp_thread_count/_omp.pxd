# distutils: language = c


cdef extern from "get_thread_count.h":
    int get_thread_count() nogil
