# input parsing
lines, i = [[]], 0
with open("input", "r") as f:
    for line in f.readlines():
        if line == "\n":
            i += 1
            lines.append([])
        else:
            lines[i].append(int(line))

# part one
sums = list(map(sum, lines))
print(max(sums))

# part two
res = 0
for i in range(3):
    m = max(sums)
    res += m
    sums.remove(m)
print(res)
