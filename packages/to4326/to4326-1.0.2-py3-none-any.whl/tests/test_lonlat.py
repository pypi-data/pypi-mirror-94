import pytest
from to4326.exceptions import *
import to4326.lonlat as lonlat


def test_warp_within():
    assert lonlat._warp_within(60) == 60
    assert lonlat._warp_within(-60) == -60
    assert lonlat._warp_within(180) == 180
    assert lonlat._warp_within(-180) == -180
    assert lonlat._warp_within(360) == 0
    assert lonlat._warp_within(-360) == 0
    assert lonlat._warp_within(-240) == 120
    assert lonlat._warp_within(240) == -120


def test_is_crossing_antimeridian():
    assert lonlat._is_crossing_antimeridian(-160, 160)
    assert lonlat._is_crossing_antimeridian(-160, -200)
    assert not lonlat._is_crossing_antimeridian(-160, -180)
    assert not lonlat._is_crossing_antimeridian(-160, 10)
    assert not lonlat._is_crossing_antimeridian(-10, 10)
    assert not lonlat._is_crossing_antimeridian(160, 180)
    assert lonlat._is_crossing_antimeridian(-160, 170)
    assert lonlat._is_crossing_antimeridian(160, 200)


def test_crossing_antimeridian_point_lat():
    assert lonlat._crossing_antimeridian_point_lat([-150, 10], [170, 10]) == 10
    assert lonlat._crossing_antimeridian_point_lat([-150, 0], [170, 20]) == 15
    assert lonlat._crossing_antimeridian_point_lat([-10, 0], [10, 170]) == 85
    assert lonlat._crossing_antimeridian_point_lat([-20, 66], [10, 0]) == 34
    assert lonlat._crossing_antimeridian_point_lat([-160, 32], [170, 20]) == 24


def test_cut_ring_at_antimeridian():
    assert lonlat.cut_ring_at_antimeridian(
        [[-160, 40], [175, 40], [-175, 35], [175, 30], [-160, 30], [-160, 40]]
    ) == lonlat.Ring(
        within=[
            [[180, 40.0], [175, 40], [180, 37.5], [180, 40.0]],
            [[180, 32.5], [175, 30], [180, 30.0], [180, 32.5]],
        ],
        overflow=[
            [
                [-180, 30.0],
                [-160, 30],
                [-160, 40],
                [-180, 40.0],
                [-180, 37.5],
                [-175, 35],
                [-180, 32.5],
                [-180, 30.0],
            ]
        ],
    )
    assert lonlat.cut_ring_at_antimeridian(
        [
            [-160, 40],
            [175, 40],
            [-1, 40],
            [-1, 35],
            [45, 35],
            [-175, 35],
            [175, 30],
            [-160, 30],
            [-160, 40],
        ]
    ) == lonlat.Ring(
        within=[
            [
                [180, 40.0],
                [175, 40],
                [-1, 40],
                [-1, 35],
                [45, 35],
                [180, 35],
                [180, 40.0],
            ],
            [[180, 32.5], [175, 30], [180, 30.0], [180, 32.5]],
        ],
        overflow=[
            [
                [-180, 30.0],
                [-160, 30],
                [-160, 40],
                [-180, 40.0],
                [-180, 35.0],
                [-175, 35],
                [-180, 32.5],
                [-180, 30.0],
            ]
        ],
    )
    assert lonlat.cut_ring_at_antimeridian(
        [[-160, 40], [175, 40], [175, 30], [-160, 30], [-160, 40]]
    ) == lonlat.Ring(
        within=[[[180, 40.0], [175, 40], [175, 30], [180, 30.0], [180, 40.0]]],
        overflow=[[[-180, 30.0], [-160, 30], [-160, 40], [-180, 40.0], [-180, 30.0]]],
    )
    assert lonlat.cut_ring_at_antimeridian(
        [[160, 40], [175, 40], [175, 30], [160, 30], [160, 40]]
    ) == lonlat.Ring(
        within=[[[160, 40], [175, 40], [175, 30], [160, 30], [160, 40]]], overflow=[]
    )
    assert lonlat.cut_ring_at_antimeridian(
        [[-10, 30], [15, 30], [15, 40], [-10, 40], [-10, 30]]
    ) == lonlat.Ring(
        within=[[[-10, 30], [15, 30], [15, 40], [-10, 40], [-10, 30]]], overflow=[]
    )
    assert lonlat.cut_ring_at_antimeridian(
        [[-160, 40], [175, 40], [-175, 30], [175, 30], [-160, 30], [-160, 40]],
        allow_selfintersection=True,
    ) == lonlat.Ring(
        within=[
            [[180, 40.0], [175, 40], [180, 35.0], [180, 40.0]],
            [[180, 30.0], [175, 30], [180, 30.0], [180, 30.0]],
        ],
        overflow=[
            [
                [-180, 30.0],
                [-160, 30],
                [-160, 40],
                [-180, 40.0],
                [-180, 35.0],
                [-175, 30],
                [-180, 30.0],
                [-180, 30.0],
            ]
        ],
    )
    assert lonlat.cut_ring_at_antimeridian(
        [[-160, 40], [-160, 30], [175, 30], [-175, 35], [175, 40], [-160, 40]]
    ) == lonlat.Ring(
        within=[
            [[180, 30.0], [175, 30], [180, 32.5], [180, 30.0]],
            [[180, 37.5], [175, 40], [180, 40.0], [180, 37.5]],
        ],
        overflow=[
            [
                [-180, 32.5],
                [-175, 35],
                [-180, 37.5],
                [-180, 40.0],
                [-160, 40],
                [-160, 30],
                [-180, 30.0],
                [-180, 32.5],
            ]
        ],
    )


def test_invalid_error():
    with pytest.raises(InvalidSelfintersection):
        lonlat.cut_ring_at_antimeridian(
            [[-160, 40], [175, 40], [-175, 30], [175, 30], [-160, 30], [-160, 40]]
        )
