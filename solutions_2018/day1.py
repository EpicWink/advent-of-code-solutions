import pathlib
import logging as lg

import _common

_logger = lg.getLogger(__name__)


def final_freq(changes):
    return sum(changes)


def get_first_duplicate_freq(changes):
    cur_freq = 0
    visited_freqs = set()
    while True:
        for change in changes:
            if cur_freq in visited_freqs:
                return cur_freq
            visited_freqs.add(cur_freq)
            cur_freq += change


def main():
    _common.setup_logging()

    data_str = pathlib.Path("input_day1.txt").read_text()
    data = list(map(int, data_str.splitlines()))

    with _common.LogTime("Part 1"):
        print("Answer pt1:", final_freq(data))

    with _common.LogTime("Part 2"):
        print("Answer pt2:", get_first_duplicate_freq(data))


if __name__ == "__main__":
    main()
