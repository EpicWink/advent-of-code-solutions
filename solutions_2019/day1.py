"""Day 1 solution.

https://adventofcode.com/2019/day/1
"""

import typing as t
import logging as lg

import _common

_logger = lg.getLogger(__name__)


def get_fuel_required(module_mass: float) -> float:
    """Get the fuel required for a module.

    Args:
        module_mass: module mass

    Returns:
        fueld required to take off
    """

    return int(module_mass / 3.0) - 2.0


def part_1(module_masses: t.List[float]) -> float:  # TODO: unit-test, document
    return sum(get_fuel_required(mass) for mass in module_masses)


def get_fuel_required_including_self(module_mass: float) -> float:
    """Get the fuel required for a module.

    Takes into account the fuel required by the fuel itself.

    Args:
        module_mass: module mass

    Returns:
        fueld required to take off
    """

    fuel = get_fuel_required(module_mass)
    if fuel <= 0.0:
        return 0.0
    return fuel + get_fuel_required_including_self(fuel)


def part_2(module_masses: t.List[float]) -> float:  # TODO: unit-test, document
    return sum(get_fuel_required_including_self(mass) for mass in module_masses)


def main():  # pragma: no cover
    _common.setup_logging()
    data_str = _common.get_input_file()
    data = list(map(float, data_str.splitlines()))

    with _common.LogTime("Part 1"):
        print("Answer pt1:", part_1(data))

    with _common.LogTime("Part 2"):
        print("Answer pt2:", part_2(data))


if __name__ == "__main__":  # pragma: no cover
    main()
