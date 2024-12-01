from os import getenv
from collections import Counter

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    lists = ([], [])
    for line in f.readlines():
        parts = line.split(" ")
        lists[0].append(int(parts[0]))
        lists[1].append(int(parts[3].strip()))

s_lists = (sorted(lists[0]), sorted(lists[1]))
res = 0

while len(s_lists[0]) > 0:
    a = min(s_lists[0])
    b = min(s_lists[1])
    s_lists[0].remove(a)
    s_lists[1].remove(b)
    d = abs(a - b)
    res += d

print(res)

counters = (Counter(lists[0]), Counter(lists[1]))

res = 0
for n, count in counters[0].items():
    res += n * count * counters[1][n]

print(res)
