with open("input_day1.txt", "r") as f:
	data = list(map(float, f.readlines()))

while True:
    for el in data:
            if cur in vals:
                    print(cur)
                    break
            vals.add(cur)
            cur += el
    else:
            continue
    break

