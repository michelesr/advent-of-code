from os import getenv
from collections import Counter

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    lists = ([], [])
    for line in f.readlines():
        parts = line.split(" ")
        lists[0].append(int(parts[0]))
        lists[1].append(int(parts[3].strip()))

lists = (sorted(lists[0]), sorted(lists[1]))
print(sum([abs(a - b) for a, b in zip(*lists)]))

counters = (Counter(lists[0]), Counter(lists[1]))
print(sum([n * count * counters[1][n] for n, count in counters[0].items()]))
