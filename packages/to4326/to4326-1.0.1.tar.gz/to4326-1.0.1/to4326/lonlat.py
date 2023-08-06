from dataclasses import dataclass
from .types import *
from .calc import *
from .utils import *
from .exceptions import *
from . import validate


def _warp_within(lon: float):
    while lon < -180:
        lon = lon + 360
    while 180 < lon:
        lon = lon - 360
    return lon


def _is_crossing_antimeridian(lon1: float, lon2: float):
    """
    The distance in the longitude between the points must be less than 180deg.

    lon1=-10, lon2=10 -> False
    lon1=170, lon2=190 -> True
    lon1=170, lon2=-170 -> True
    """
    if abs(lon1 - lon2) > 360:
        return True
    lon1 = _warp_within(lon1)
    lon2 = _warp_within(lon2)

    if lon1 * lon2 > 0:
        return False

    return abs(lon1 - lon2) > 180


def _crossing_antimeridian_point_lat(p1: Point, p2: Point):
    """
    p1=[-150, 0], p2=[170, 20]) -> 15
    p1=[-20,-10], p2=[10, 170] -> 85
    p1=[-20, 66], p2=[10, 0]) -> 34
    p1=[-160, 32], p2=[170, 20]) -> 24
    """
    [x1, y1] = p1
    [x2, y2] = p2
    if x1 < 0:
        x1 = _warp_within(x1) + 360
    if x2 < 0:
        x2 = _warp_within(x2) + 360
    return linear_y([x1, y1], [x2, y2], 180)


@dataclass
class Ring:
    within: list
    overflow: list


def cut_ring_at_antimeridian(
    linear_ring: Points, overflowing: bool = False, allow_selfintersection: bool = False
):
    """
    When overflowing is True, points are right side of 180 degrees.
    The overflowing flag is used when recursive.
    The distance in the longitude between the points must be less than 180deg.
    """
    validate.linear_ring(linear_ring)

    crossing_lats = []

    for i in range(len(linear_ring) - 1):
        if _is_crossing_antimeridian(linear_ring[i][0], linear_ring[i + 1][0]):
            crossing_lats.append(
                {
                    "from": i,
                    "to": i + 1,
                    "lat": _crossing_antimeridian_point_lat(
                        linear_ring[i], linear_ring[i + 1]
                    ),
                }
            )
    if len(crossing_lats) < 2:
        return (
            Ring(within=[linear_ring], overflow=[])
            if not overflowing
            else Ring(within=[], overflow=[linear_ring])
        )
    crossing_lats = sorted(crossing_lats, key=lambda p: p["lat"])
    start = crossing_lats[-1]
    end = crossing_lats[-2]

    ret: Ring = Ring(within=[], overflow=[])

    def _cutting(start, end):
        ring_index = start["to"] if not start["to"] == len(linear_ring) - 1 else 0
        bound_lon = 180 if linear_ring[ring_index][0] >= 0 else -180

        rtn = {"overflowing": bound_lon < 0, "linear_ring": []}
        rtn["linear_ring"].append(
            [
                bound_lon,
                _crossing_antimeridian_point_lat(
                    linear_ring[start["from"]], linear_ring[start["to"]]
                ),
            ]
        )
        rtn["linear_ring"].append(linear_ring[start["to"]])

        while ring_index != end["from"]:
            ring_index = (
                ring_index + 1 if not ring_index + 1 == len(linear_ring) - 1 else 0
            )
            rtn["linear_ring"].append(linear_ring[ring_index])
        rtn["linear_ring"].append(
            [
                bound_lon,
                _crossing_antimeridian_point_lat(
                    linear_ring[end["from"]], linear_ring[end["to"]]
                ),
            ]
        )
        rtn["linear_ring"].append(rtn["linear_ring"][0])
        return rtn

    cut1 = _cutting(start, end)
    result1 = cut_ring_at_antimeridian(
        cut1["linear_ring"],
        cut1["overflowing"],
        allow_selfintersection=allow_selfintersection,
    )
    ret.within.extend(result1.within)
    ret.overflow.extend(result1.overflow)

    cut2 = _cutting(end, start)
    result2 = cut_ring_at_antimeridian(
        cut2["linear_ring"],
        cut2["overflowing"],
        allow_selfintersection=allow_selfintersection,
    )
    ret.within.extend(result2.within)
    ret.overflow.extend(result2.overflow)

    if not allow_selfintersection:
        for ring in ret.within:
            if selfintersection(ring):
                raise InvalidSelfintersection

        for ring in ret.overflow:
            if selfintersection(ring):
                raise InvalidSelfintersection

    return ret