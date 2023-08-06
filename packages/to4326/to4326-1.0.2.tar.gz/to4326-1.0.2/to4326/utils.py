import math
from .types import *
from .constants import *
from . import validate


def is_ccw(linear_ring: Points):
    validate.linear_ring(linear_ring)
    area = 0.0

    length = len(linear_ring) - 1

    for i in range(length - 1):
        area = (
            area
            + linear_ring[i][0] * linear_ring[i + 1][1]
            - linear_ring[i][1] * linear_ring[i + 1][0]
        )

    area = (
        area
        + linear_ring[length - 1][0] * linear_ring[0][1]
        - linear_ring[length - 1][1] * linear_ring[0][0]
    )

    return area >= 0


def within(point: Point, linear_ring: Points, include_border: bool = False):
    """
    Winding Number Algorithm
    """
    validate.points([point])
    validate.linear_ring(linear_ring)
    [x, y] = point
    theta: float = 0
    for i in range(len(linear_ring)):
        x1, y1 = linear_ring[i - 1]
        x2, y2 = linear_ring[i]
        x1 -= x
        y1 -= y
        x2 -= x
        y2 -= y

        cv = x1 * x2 + y1 * y2
        sv = x1 * y2 - x2 * y1
        if abs(sv) < EPSILON and cv <= 0:
            return include_border
        theta += math.atan2(sv, cv)
    return abs(theta) > 1


def intersection(p1: Point, p2: Point, p3: Point, p4: Point):
    """
    When p1 -> p2, p3 -> p4 are crossing or points more than 3 are on a line,
    return True
    """
    validate.points([p1, p2, p3, p4])
    if p1[0] >= p2[0]:
        if (p1[0] < p3[0] and p1[0] < p4[0]) or (p2[0] > p3[0] and p2[0] > p4[0]):
            return False
    else:
        if (p2[0] < p3[0] and p2[0] < p4[0]) or (p1[0] > p3[0] and p1[0] > p4[0]):
            return False

    if p1[1] >= p2[1]:
        if (p1[1] < p3[1] and p1[1] < p4[1]) or (p2[1] > p3[1] and p2[1] > p4[1]):
            return False
    else:
        if (p2[1] < p3[1] and p2[1] < p4[1]) or (p1[1] > p3[1] and p1[1] > p4[1]):
            return False

    if ((p1[0] - p2[0]) * (p3[1] - p1[1]) + (p1[1] - p2[1]) * (p1[0] - p3[0])) * (
        (p1[0] - p2[0]) * (p4[1] - p1[1]) + (p1[1] - p2[1]) * (p1[0] - p4[0])
    ) > 0:
        return False
    if ((p3[0] - p4[0]) * (p1[1] - p3[1]) + (p3[1] - p4[1]) * (p3[0] - p1[0])) * (
        (p3[0] - p4[0]) * (p2[1] - p3[1]) + (p3[1] - p4[1]) * (p3[0] - p2[0])
    ) > 0:
        return False

    return True


def selfintersection(linear_ring: Points):
    """
    not support warp polygon.
    """
    validate.linear_ring(linear_ring)
    if len(linear_ring) == 4:
        return (
            abs(
                linear_ring[0][1] * (linear_ring[1][0] - linear_ring[2][0])
                + linear_ring[1][1] * (linear_ring[2][0] - linear_ring[0][0])
                + linear_ring[2][1] * (linear_ring[0][0] - linear_ring[1][0])
            )
            < EPSILON
        )

    lines = [[linear_ring[i], linear_ring[i + 1]] for i in range(len(linear_ring) - 2)]

    def check(lines, start=0):
        if start + 2 >= len(lines):
            return False

        l1 = lines[start]
        for i in range(start + 2, len(lines)):
            l2 = lines[i]
            if intersection(*l1, *l2):
                return True
        return check(lines, start + 1)

    return check(lines)