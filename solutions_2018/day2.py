with open("input_day2.txt", "r") as f:
	words = f.readlines()

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
checksum = counts2 * counts3
print("checksum:", checksum)

for j, word in enumerate(words):
	for word2 in words[j + 1:]:
		difference = 0
		for l in range(len(word)):
			if word[l] != word2[l]:
				difference += 1
		if difference < 2:
			print(word, word2, "difference:", difference)
			for l in range(len(word)):
				if word[l] == word2[l]:
					print(word[l], end="")
