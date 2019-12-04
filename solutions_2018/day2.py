"""Day 2 solution.

https://adventofcode.com/2018/day/2
"""

import logging as lg

import _common

_logger = lg.getLogger(__name__)


def compute_checksum(words):  # TODO: document
    counts2 = 0
    counts3 = 0
    for word in words:
        letters = {}
        for letter in word:
            if letter not in letters:
                letters[letter] = 0
            letters[letter] += 1
        if any(c == 2 for c in letters.values()):
            counts2 += 1
        if any(c == 3 for c in letters.values()):
            counts3 += 1
    return counts2 * counts3


def get_same_boxes_common_characters(words):  # TODO: document
    for j, word in enumerate(words):
        for word2 in words[j + 1:]:
            difference = 0
            for l in range(len(word)):
                if word[l] != word2[l]:
                    difference += 1
            if difference < 2:
                _logger.debug("{} / {} difference: {}".format(word, word2, difference))
                common_chars = []
                for l in range(len(word)):
                    if word[l] == word2[l]:
                        common_chars.append(word[l])
                return "".join(common_chars)


class Solution(_common.InputLinesSolution):  # TODO: unit-test, document
    line_type = float

    def part_1(self):
        return compute_checksum(self.items)

    def part_2(self):
        return get_same_boxes_common_characters(self.items)


def main():  # pragma: no cover
    Solution().run()


if __name__ == "__main__":  # pragma: no cover
    main()
