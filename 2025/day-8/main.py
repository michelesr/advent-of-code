from collections import Counter
from math import prod, sqrt
from os import getenv
from typing import cast

Box = tuple[int, int, int]


def distance(a: Box, b: Box) -> float:
    a1, a2, a3 = a
    b1, b2, b3 = b
    return sqrt((a1 - b1) ** 2 + (a2 - b2) ** 2 + (a3 - b3) ** 2)


def connect_pair(circuits: dict[Box, set[Box]], pair: tuple[Box, Box]) -> set[Box]:
    a, b = pair
    if circuits[a] is circuits[b]:
        return circuits[a]
    new_circuit = circuits[a] | circuits[b]
    for box in new_circuit:
        circuits[box] = new_circuit
    return new_circuit


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    boxes = [
        cast(Box, tuple(int(n) for n in line.strip().split(",")))
        for line in f.readlines()
    ]

distances: dict[tuple[Box, Box], float] = {}
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
    connect_pair(circuits, pairs.pop()[0])

c = Counter(map(tuple, circuits.values()))
print(prod(list(sorted(c.values(), reverse=True))[:3]))

# part two
L = len(boxes)
while pairs:
    pair = pairs.pop()[0]
    if len(connect_pair(circuits, pair)) == L:
        a, b = pair
        print(a[0] * b[0])
        break
