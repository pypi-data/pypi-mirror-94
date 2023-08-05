# Copyright (c) 2010-2020 Manfred Moitzi
# License: MIT License
import random

from ezdxf.math import (
    cubic_bezier_interpolation, Vec3, Bezier3P, quadratic_to_cubic_bezier,
)


def test_vertex_interpolation():
    points = [(0, 0), (3, 1), (5, 3), (0, 8)]
    result = list(cubic_bezier_interpolation(points))
    assert len(result) == 3
    c1, c2, c3 = result
    p = c1.control_points
    assert p[0].isclose((0, 0))
    assert p[1].isclose((0.9333333333333331, 0.3111111111111111))
    assert p[2].isclose((1.8666666666666663, 0.6222222222222222))
    assert p[3].isclose((3, 1))

    p = c2.control_points
    assert p[0].isclose((3, 1))
    assert p[1].isclose((4.133333333333334, 1.3777777777777778))
    assert p[2].isclose((5.466666666666667, 1.822222222222222))
    assert p[3].isclose((5, 3))

    p = c3.control_points
    assert p[0].isclose((5, 3))
    assert p[1].isclose((4.533333333333333, 4.177777777777778))
    assert p[2].isclose((2.2666666666666666, 6.088888888888889))
    assert p[3].isclose((0, 8))


def test_quadratic_to_cubic_bezier():
    r = random.Random(0)

    def random_vec() -> Vec3:
        return Vec3(r.uniform(-10, 10), r.uniform(-10, 10), r.uniform(-10, 10))

    for i in range(1000):
        quadratic = Bezier3P((random_vec(), random_vec(), random_vec()))
        quadratic_approx = list(quadratic.approximate(10))
        cubic = quadratic_to_cubic_bezier(quadratic)
        cubic_approx = list(cubic.approximate(10))

        assert len(quadratic_approx) == len(cubic_approx)
        for p1, p2 in zip(quadratic_approx, cubic_approx):
            assert p1.isclose(p2)
