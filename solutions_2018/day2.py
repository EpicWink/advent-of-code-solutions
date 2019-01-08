import logging as lg

import _common

_logger = lg.getLogger(__name__)


def compute_checksum(words):
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


def get_same_boxes_common_characters(words):
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


def main():
    _common.setup_logging()
    data_str = _common.get_input_file()
    words = data_str.splitlines()

    with _common.LogTime("Part 1"):
        print("Answer pt1:", compute_checksum(words))

    with _common.LogTime("Part 2"):
        print("Answer pt2:", get_same_boxes_common_characters(words))


if __name__ == "__main__":
    main()
