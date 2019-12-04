"""Test ``day3``."""

from solutions_2019 import day3 as tscr
import pytest
# from unittest import mock
# import numpy as np


@pytest.mark.parametrize(
    ("movements", "exp"),
    [
        (["R8,U5,L5,D3", "U7,R6,D4,L4"], 6),
        (["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"], 159),
        (["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"], 135),
    ],
)
def test_wires(movements, exp):
    movements_1, movements_2 = movements
    wires = tscr.Wires(movements_1, movements_2)
    wires.run()
    assert wires.intersection_distance == exp
