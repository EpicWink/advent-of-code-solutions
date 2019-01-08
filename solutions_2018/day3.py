with open("input_day3.txt", "r") as f:
    lines = f.readlines()

import numpy as np

yxs = [None] * len(lines)
hws = [None] * len(lines)
ids = [None] * len(lines)
for j, line in enumerate(lines):
    line = line.strip()
    id_str, _, xy_str, size_str = line.split()
    x, y = map(int, xy_str[:-1].split(","))
    w, h = map(int, size_str.split("x"))
    yxs[j] = (y, x)
    hws[j] = (h, w)
    ids[j] = id_str[1:]
yxs = np.array(yxs)
hws = np.array(hws)

max_yx = np.max(yxs + hws, axis=0)
print("max_yx:", max_yx)

counts = np.zeros(max_yx, dtype=np.int)
for (y, x), (h, w) in zip(yxs, hws):
    counts[y:y + h, x:x + w] += 1
print("n squares with more than 1 claim:", np.sum(counts > 1))

for j, ((y, x), (h, w)) in enumerate(zip(yxs, hws)):
    if np.all(counts[y:y + h, x:x + w] == 1):
        print("unique claim:", ids[j], "({})".format(((y, x), (h, w))))
