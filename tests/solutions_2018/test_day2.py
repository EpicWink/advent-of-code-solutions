from solutions_2018 import day2 as tscr
# import pytest


def test_part_1():
    words = ["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"]
    exp = 12
    assert tscr.compute_checksum(words) == exp


def test_part_2():
    words = ["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"]
    exp = "fgij"
    assert tscr.get_same_boxes_common_characters(words) == exp
