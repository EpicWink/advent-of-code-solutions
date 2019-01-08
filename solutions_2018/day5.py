with open("input_day5.txt", "r") as f:
    data = f.read().strip()

import logging as lg
lg.basicConfig(level=lg.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S")
_logger = lg.getLogger(__name__)

_logger.debug("data length: {}".format(len(data)))


def collapse(letters):
    # A = 65
    # a = 97
    j = 0
    while letters and j < len(letters) - 1:
        letter1 = letters[j]
        letter2 = letters[j + 1]
        if abs(ord(letter1) - ord(letter2)) == 32:
            letters.pop(j + 1)
            letters.pop(j)
            j -= 1
        else:
            j += 1
        if j < 0:
            j = 0


letters = list(data)
collapse(letters)
# _logger.debug("Final result: {}".format("".join(letters)))
print("Answer pt1:", len(letters))

letters = list(data)
final_lengths = []
for j in range(26):
    remove_letter_ords = (65 + j, 97 + j)
    letters_j = [l for l in letters if ord(l) not in remove_letter_ords]
    collapse(letters_j)
    _logger.debug("Removing '{}': final length: {}".format(chr(65 + j), len(letters_j)))
    final_lengths.append(len(letters_j))

print("Answer pt2:", min(final_lengths))
