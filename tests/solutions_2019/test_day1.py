"""Test ``day1``."""

from solutions_2019 import day1 as tscr
import pytest
# from unittest import mock


@pytest.mark.parametrize(
    ("module_mass", "exp"),
    [
        (12, 2),
        (14, 2),
        (1969, 654),
        (100756, 33583),
    ],
)
def test_get_fuel_required(module_mass, exp):
    res = tscr.get_fuel_required(module_mass)
    assert res == pytest.approx(exp)


@pytest.mark.parametrize(
    ("module_mass", "exp"),
    [
        (12, 2),
        (1969, 966),
        (100756, 50346),
    ],
)
def test_get_fuel_required_including_self(module_mass, exp):
    res = tscr.get_fuel_required_including_self(module_mass)
    assert res == pytest.approx(exp)
