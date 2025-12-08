from os import getenv
from collections import Counter
from math import sqrt, prod


def distance(a, b):
    a1, a2, a3 = a
    b1, b2, b3 = b
    return sqrt((a1 - b1) ** 2 + (a2 - b2) ** 2 + (a3 - b3) ** 2)


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    boxes = [tuple(int(n) for n in line.strip().split(",")) for line in f.readlines()]

distances = {}

for box in boxes:
    for other in set(boxes) - {box}:
        a, b = sorted([box, other])
        if (a, b) not in distances:
            distances[(a, b)] = distance(a, b)


# part one
pairs = sorted(distances.items(), key=lambda item: item[1], reverse=True)
circuits = {box: {box} for box in boxes}

LIMIT = 10
if len(boxes) >= 100:
    LIMIT = 1000

for i in range(LIMIT):
    a, b = pairs.pop()[0]
    new_circuit = circuits[a] | circuits[b]
    for box in new_circuit:
        circuits[box] = new_circuit

c = Counter(map(tuple, circuits.values()))
print(prod(list(sorted(c.values(), reverse=True))[:3]))

# part two
pairs = sorted(distances.items(), key=lambda item: item[1], reverse=True)
circuits = {box: {box} for box in boxes}

L = len(boxes)

while pairs:
    a, b = pairs.pop()[0]
    new_circuit = circuits[a] | circuits[b]
    for box in new_circuit:
        circuits[box] = new_circuit
    if len(new_circuit) == L:
        print(a[0] * b[0])
        break
