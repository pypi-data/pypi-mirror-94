# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
from eelbrain._utils.parse import find_variables


def test_find_variables():
    assert find_variables("a + b / c.x()") == {'a', 'b', 'c'}
    assert find_variables("a + 'b' / c.x()") == {'a', 'c'}
