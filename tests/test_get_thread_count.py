from omp_thread_count import get_thread_count


def test_get_thread_count():
    count = get_thread_count()
    assert count > 0
