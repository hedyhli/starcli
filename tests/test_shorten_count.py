"""tests.test_shorten_count"""
from starcli.layouts import shorten_count


def test_shorten_count():
    """Test the shorten_count functionality"""
    assert shorten_count(1487) == "1.5k"
    assert shorten_count(6001) == "6k"
    assert shorten_count(15587) == "15.6k"
    assert shorten_count(12) == "12"
