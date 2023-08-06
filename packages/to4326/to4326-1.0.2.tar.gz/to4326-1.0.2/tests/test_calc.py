import pytest
from to4326.exceptions import *
from to4326.calc import *


def test_linear_x():
    assert linear_x([0, 0], [10, 10], 5) == 5
    assert linear_x([0, 0], [10, 10], 20) == 20
    assert linear_x([0, 0], [10, 0], -5) == 0
    assert linear_x([-10, 0], [10, 10], 5) == 0


def test_linear_y():
    assert linear_y([0, 0], [10, 10], 5) == 5
    assert linear_y([0, 0], [10, 10], 20) == 20
    assert linear_y([0, 0], [0, 10], -5) == 0
    assert linear_y([-10, 0], [10, 10], 5) == 7.5


def test_linear_interpolate():
    assert linear_interpolate([0, 0], [10, 10]) == [[0, 0], [10, 10]]
    assert linear_interpolate([0, 0], [1, 1], 9) == [
        [0, 0],
        [0.1, 0.1],
        [0.2, 0.2],
        [0.3, 0.3],
        [0.4, 0.4],
        [0.5, 0.5],
        [0.6, 0.6],
        [0.7, 0.7],
        [0.8, 0.8],
        [0.9, 0.9],
        [1, 1],
    ]
    assert linear_interpolate([10, 10], [-10, -10], 4) == [
        [10, 10],
        [6, 6],
        [2, 2],
        [-2, -2],
        [-6, -6],
        [-10, -10],
    ]


def test_invalid_error():
    with pytest.raises(InvalidPoint):
        linear_x([0, 0], [10, 10, 4], 5)
    with pytest.raises(InvalidPoint):
        linear_x([0], [10, 10], 5)
    with pytest.raises(InvalidPoint):
        linear_y([0, 0, 5], [10, 10], 5)
    with pytest.raises(InvalidPoint):
        linear_y([0, 0, 5], [10], 5)
    with pytest.raises(InvalidPoint):
        linear_interpolate([0, 0], [10])
    with pytest.raises(InvalidPoint):
        linear_interpolate([0, 0, 5], [10, 10])
