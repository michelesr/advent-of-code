from os import getenv
from collections import Counter

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    # parse the input into two lists
    lists = ([], [])
    for line in f.readlines():
        parts = line.split(" ")
        lists[0].append(int(parts[0]))
        lists[1].append(int(parts[3].strip()))

# -- part one --

# sort the lists
lists = (sorted(lists[0]), sorted(lists[1]))

# calculate distance for each pair and sum them
print(sum([abs(a - b) for a, b in zip(*lists)]))

# -- part two --

# calculate frequency of each item in the lists
counters = (Counter(lists[0]), Counter(lists[1]))

# calculate the similarity scores and sum them
print(sum([n * count * counters[1][n] for n, count in counters[0].items()]))
