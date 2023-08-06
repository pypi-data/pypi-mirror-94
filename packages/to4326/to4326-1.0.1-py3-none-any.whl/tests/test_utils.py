from to4326.validate import *
from to4326.utils import *


def test_is_ccw():
    assert is_ccw([[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]])
    assert not is_ccw([[-10, -10], [-10, 10], [10, 10], [10, -10], [-10, -10]])
    assert not is_ccw([[170, -10], [-170, -10], [-170, 10], [170, 10], [170, -10]])


def test_within():
    assert within([0, 0], [[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]])
    assert not within(
        [0, 100], [[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]]
    )
    assert not within(
        [-10, -10], [[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]]
    )
    assert within(
        [-10, -10],
        [[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]],
        include_border=True,
    )
    assert not within(
        [0, -10], [[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]]
    )
    assert within(
        [0, -10],
        [[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]],
        include_border=True,
    )
    assert within([0, 0], [[170, -10], [-170, -10], [-170, 10], [170, 10], [170, -10]])
    assert not within(
        [180, 0], [[170, -10], [-170, -10], [-170, 10], [170, 10], [170, -10]]
    )
    assert not within(
        [-180, 0], [[170, -10], [-170, -10], [-170, 10], [170, 10], [170, -10]]
    )


def test_intersection():
    assert intersection([0, 0], [10, 10], [1, 8], [9, 2])
    assert not intersection([0, 0], [10, 10], [1, 8], [-9, 2])
    assert intersection([0, 0], [10, 10], [1, 8], [5, 5])
    assert not intersection([0, 0], [10, 10], [1, 8], [4, 5])
    assert intersection([0, 0], [10, 10], [2, 2], [5, 5])
    assert intersection([0, 0], [10, 10], [-2, -2], [5, 5])


def test_selfintersection():
    assert not selfintersection(
        [[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]]
    )
    assert not selfintersection(
        [[-10, -10], [-10, 10], [10, 10], [10, -10], [-10, -10]]
    )
    assert not selfintersection(
        [[-10, -10], [10, -10], [10, 10], [0, 10], [-10, 10], [-10, -10]]
    )
    assert selfintersection(
        [[-10, -10], [10, -10], [10, 10], [0, -10], [-10, 10], [-10, -10]]
    )
    assert selfintersection([[-10, -10], [10, -10], [20, -10], [-10, -10]])
