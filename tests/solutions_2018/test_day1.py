from solutions_2018 import day1 as tscr
import pytest


@pytest.mark.parametrize(("changes", "exp"), [
    ([1, -2, 3, 1], 3),
    ([1, 1, 1], 3),
    ([1, 1, -2], 0),
    ([-1, -2, -3], -6)])
def test_part_1(changes, exp):
    assert tscr.final_freq(changes) == exp


@pytest.mark.parametrize(("changes", "exp"), [
    ([1, -2, 3, 1], 2),
    ([1, -1], 0),
    ([3, 3, 4, -2, -4], 10),
    ([-6, 3, 8, 5, -6], 5),
    ([7, 7, -2, -7, -4], 14)])
def test_part_2(changes, exp):
    assert tscr.get_first_duplicate_freq(changes) == exp
