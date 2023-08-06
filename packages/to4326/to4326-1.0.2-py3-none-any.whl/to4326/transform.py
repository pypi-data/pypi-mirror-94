import sys
from functools import reduce
from typing import Sequence
from pyproj import CRS, Transformer
from .types import *
from .exceptions import *
from .constants import *
from .utils import *
from .calc import *
from .lonlat import *
from . import validate


def _transform(points: Points, src_crs: CRS, dst_crs: CRS):
    if src_crs == dst_crs:
        return points
    transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)

    return [list(transformer.transform(*p)) for p in points]


def _transform_enclosing_pole_ring(
    linear_ring: Points, src_crs: CRS, partition: int, north: bool = True
):
    length = len(linear_ring) - 1
    temp_CRS = (
        ARCTIC_POLAR_STEROGRAPHIC_CRS if north else ANTARCTIC_POLAR_STEROGRAPHIC_CRS
    )

    end_y = sys.maxsize if north else -1 * sys.maxsize
    pole_lat = 90 if north else -90
    polar_sterographic_linear_ring = _transform(linear_ring, src_crs, temp_CRS)

    crossing_ys = []
    for i in range(length):
        if intersection(
            polar_sterographic_linear_ring[i],
            polar_sterographic_linear_ring[i + 1],
            [0, 0],
            [0, end_y],
        ):
            crossing_ys.append(
                {
                    "from": i,
                    "to": i + 1,
                    "y": linear_y(
                        polar_sterographic_linear_ring[i],
                        polar_sterographic_linear_ring[i + 1],
                        0,
                    ),
                }
            )
    if not len(crossing_ys) == 1:
        # not support linear ring that is not enclosing the pole and straddling the antimeridian many times.
        raise InvalidLinearRingEnclosingPole
    crossing_ys = sorted(crossing_ys, key=lambda p: p["y"])
    crossing_y = crossing_ys[-1] if north else crossing_ys[0]

    ret = []
    for i in range(length):
        if i == crossing_y["from"]:
            transformed = _transform(
                linear_interpolate(
                    polar_sterographic_linear_ring[crossing_y["from"]],
                    [0, crossing_y["y"]],
                    partition,
                ),
                temp_CRS,
                EPSG4326_CRS,
            )

            ret.extend(transformed[:-1])
            if transformed[0][0] >= 0:
                ret.extend(
                    [
                        [180, transformed[-1][1]],
                        [180, pole_lat],
                        [-180, pole_lat],
                        [-180, transformed[-1][1]],
                    ]
                )
            else:
                ret.extend(
                    [
                        [-180, transformed[-1][1]],
                        [-180, pole_lat],
                        [180, pole_lat],
                        [180, transformed[-1][1]],
                    ]
                )
            ret.extend(
                _transform(
                    linear_interpolate(
                        [0, crossing_y["y"]],
                        polar_sterographic_linear_ring[crossing_y["to"]],
                        partition,
                    ),
                    temp_CRS,
                    EPSG4326_CRS,
                )[1:-1]
            )
        else:
            ret.extend(
                _transform(
                    linear_interpolate(
                        polar_sterographic_linear_ring[i],
                        polar_sterographic_linear_ring[i + 1],
                        partition,
                    ),
                    temp_CRS,
                    EPSG4326_CRS,
                )[:-1]
            )
    ret.append(ret[0])

    return ret


def transform_ring(linear_ring: Points, src_crs: CRS, partition: int = 0):
    """
    not support linear rings of including both poles.
    """
    validate.linear_ring(linear_ring)
    length = len(linear_ring) - 1

    north_pole = _transform([[0, 90]], EPSG4326_CRS, src_crs)[0]
    enclosing_north_pole = within(north_pole, linear_ring)
    south_pole = _transform([[0, -90]], EPSG4326_CRS, src_crs)[0]
    enclosing_south_pole = within(south_pole, linear_ring)
    if enclosing_north_pole and enclosing_south_pole:
        raise EnclosingBothPoles

    if enclosing_north_pole:
        return _transform_enclosing_pole_ring(
            linear_ring, src_crs, partition=partition, north=True
        )
    if enclosing_south_pole:
        return _transform_enclosing_pole_ring(
            linear_ring, src_crs, partition=partition, north=False
        )

    interpolated_linear_ring = []
    for i in range(length):
        interpolated_linear_ring.extend(
            linear_interpolate(linear_ring[i], linear_ring[i + 1], partition)[:-1]
        )
    interpolated_linear_ring.append(interpolated_linear_ring[0])

    if src_crs == EPSG4326_CRS:
        return interpolated_linear_ring

    return _transform(interpolated_linear_ring, src_crs, EPSG4326_CRS)


def transform_bbox(
    src_bbox: Sequence[float], src_crs: CRS, partition: int = 9, expand: bool = False
):
    """
    input bbox is not allowed warp.
    """
    if not (len(src_bbox) == 4 or len(src_bbox) == 6):
        raise InvalidBounds

    has_height = len(src_bbox) == 6
    left = src_bbox[0]
    bottom = src_bbox[1]
    right = src_bbox[3] if has_height else src_bbox[2]
    top = src_bbox[4] if has_height else src_bbox[3]

    if right < left:
        raise NotAllowedWarpBounds

    points = transform_ring(
        [[left, bottom], [right, bottom], [right, top], [left, top], [left, bottom]],
        src_crs,
        partition=partition,
    )

    ys = [p[1] for p in points]
    if is_ccw(points):
        xs = [p[0] for p in points]
        if len(src_bbox) == 6:
            return [min(xs), min(ys), src_bbox[2], max(xs), max(ys), src_bbox[5]]
        return [min(xs), min(ys), max(xs), max(ys)]

    try:
        bounds_ring = cut_ring_at_antimeridian(points)
        xs1 = [p[0] for p in reduce(lambda a, b: a + b, bounds_ring.within)]
        xs2 = [p[0] for p in reduce(lambda a, b: a + b, bounds_ring.overflow)]
        if len(src_bbox) == 6:
            return [
                min(xs1),
                min(ys),
                src_bbox[2],
                max(xs2) + 360 if expand else max(xs2),
                max(ys),
                src_bbox[5],
            ]
        return [min(xs1), min(ys), max(xs2) + 360 if expand else max(xs2), max(ys)]
    except:
        raise FalidCuttingAntimeridian


def geojson_from_linear_ring(linear_ring: Points, src_crs: CRS, partition: int = 9):
    if not is_ccw(linear_ring):
        raise NotAllowedCwLinearRing
    points = transform_ring(linear_ring, src_crs, partition=partition)
    ys = [p[1] for p in points]

    if is_ccw(points):
        xs = [p[0] for p in points]
        return {
            "type": "Feature",
            "bbox": [min(xs), min(ys), max(xs), max(ys)],
            "properties": {},
            "geometry": {"type": "Polygon", "coordinates": [points]},
        }

    try:
        ring = cut_ring_at_antimeridian(points)
        xs1 = [p[0] for p in reduce(lambda a, b: a + b, ring.within)]
        xs2 = [p[0] for p in reduce(lambda a, b: a + b, ring.overflow)]
        coordinates = []
        coordinates.extend([[r] for r in ring.within])
        coordinates.extend([[r] for r in ring.overflow])
        return {
            "type": "Feature",
            "bbox": [min(xs1), min(ys), max(xs2), max(ys)],
            "properties": {},
            "geometry": {"type": "MultiPolygon", "coordinates": coordinates},
        }

    except:
        raise FalidCuttingAntimeridian


def geojson_from_corner_coordinates(
    upper_left: Point,
    lower_left: Point,
    upper_right: Point,
    lower_right: Point,
    src_crs: CRS,
    partition: int = 9,
):
    return geojson_from_linear_ring(
        [upper_left, lower_left, lower_right, upper_right, upper_left],
        src_crs,
        partition=partition,
    )
