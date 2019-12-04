"""Day 1 solution.

https://adventofcode.com/2018/day/1
"""

import _common


def final_freq(changes: list):
    """Compute the final frequency.

    Args:
        changes: frequency changes

    Returns:
        sum of changes
    """

    return sum(changes)


def get_first_duplicate_freq(changes: list):
    """Find the first duplicate frequency.

    Args:
        changes: frequency changes

    Returns:
        first duplicate frequency
    """

    cur_freq = 0
    visited_freqs = set()
    while True:
        for change in changes:
            if cur_freq in visited_freqs:
                return cur_freq
            visited_freqs.add(cur_freq)
            cur_freq += change


class Solution(_common.InputLinesSolution):  # TODO: unit-test, document
    line_type = int

    def part_1(self):
        return sum(self.items)

    def part_2(self):
        return get_first_duplicate_freq(self.items)


main = Solution.main
if __name__ == "__main__":  # pragma: no cover
    main()
