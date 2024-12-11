from os import getenv
from copy import copy
from collections import Counter

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    numbers = [int(n) for n in f.read().split(" ")]

counts = Counter(numbers)
map = {}


def iter():
    for k, v in copy(counts).items():
        if k in map.keys():
            a, b = map[k]
        else:
            if k == 0:
                res = k + 1, None
            elif len(str(k)) % 2 == 0:
                s = str(k)
                l = len(s)
                res = int(s[: l // 2]), int(s[l // 2 :])
            else:
                res = k * 2024, None
            map[k] = res
            a, b = res
        counts[k] -= v
        if counts[k] == 0:
            del counts[k]
        counts[a] += v
        if b is not None:
            counts[b] += v


for i in range(25):
    iter()

print(sum(v for v in counts.values()))

for i in range(75 - 25):
    iter()

print(sum(v for v in counts.values()))
