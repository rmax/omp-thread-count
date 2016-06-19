"""The purpose of this is to ensure _test_cimport was build correctly."""
from ._test_cimport import get_thread_count

def test_get_thread_count():
    assert get_thread_count() > 0
