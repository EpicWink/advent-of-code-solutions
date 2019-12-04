"""Day 1 solution.

https://adventofcode.com/2019/day/1
"""

import _common


def get_fuel_required(module_mass: float) -> float:
    """Get the fuel required for a module.

    Args:
        module_mass: module mass

    Returns:
        fueld required to take off
    """

    return int(module_mass / 3.0) - 2.0


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


class Solution(_common.InputLinesSolution):  # TODO: unit-test, document
    line_type = float
    year = 2019
    day = 1

    def part_1(self):
        return sum(get_fuel_required(mass) for mass in self.items)

    def part_2(self):
        return sum(get_fuel_required_including_self(mass) for mass in self.items)


main = Solution.main
if __name__ == "__main__":  # pragma: no cover
    main()
