import omp_thread_count


def test_get_thread_count():
    count = omp_thread_count.get_thread_count()
    assert count > 0


def test_get_includes():
    dirs = omp_thread_count.get_includes()
    # Whether this dirs actually work is done in the cimport test.
    assert dirs
