from .types import *
from . import validate


def linear_x(p1: Point, p2: Point, y: float):
    validate.points([p1, p2])
    if p2[1] == p1[1]:
        return p1[0]
    return p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])


def linear_y(p1: Point, p2: Point, x: float):
    validate.points([p1, p2])
    if p2[0] == p1[0]:
        return p1[1]
    return p1[1] + (x - p1[0]) * (p2[1] - p1[1]) / (p2[0] - p1[0])


def linear_interpolate(p1: Point, p2: Point, partition: int = 0):
    validate.points([p1, p2])

    if partition <= 0:
        return [p1, p2]
    ret = []

    def calc(i):
        if p2[0] == p1[0]:
            x = p1[0]
            y = p1[1] + i * (p2[1] - p1[1]) / (partition + 1)
        elif p2[1] == p1[1]:
            x = p1[0] + i * (p2[0] - p1[0]) / (partition + 1)
            y = p1[1]
        else:
            x = p1[0] + i * (p2[0] - p1[0]) / (partition + 1)
            y = linear_y(p1, p2, x)

        return [x, y]

    ret = [calc(i) for i in range(partition + 1)]
    ret.append(p2)
    return ret