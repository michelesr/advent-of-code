from os import getenv
import itertools

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    grid = [list(line.strip()) for line in f.readlines()]

I = len(grid)
J = len(grid[0])


def get_antinodes(
    a: tuple[int, int], b: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    a, b = sorted((a, b))
    x1, y1 = a
    x2, y2 = b

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    if a == b:
        raise ValueError("same point")

    x3, x4 = min(x1, x2) - dx, max(x1, x2) + dx

    if y1 > y2:
        x3, x4 = x4, x3

    y3, y4 = min(y1, y2) - dy, max(y1, y2) + dy
    return ((x3, y3), (x4, y4))


def is_in_grid(i, j):
    return 0 <= i < I and 0 <= j < J


antennas = {}
for i in range(I):
    for j in range(J):
        spot = grid[i][j]
        if spot != ".":
            if spot not in antennas.keys():
                antennas[spot] = []
            antennas[spot].append((i, j))

# part 1
antinodes = set()
for k, v in antennas.items():
    comb = itertools.combinations(v, 2)
    for a, b in comb:
        for antinode in get_antinodes(a, b):
            if is_in_grid(*antinode):
                antinodes.add(antinode)

print(len(antinodes))

# part 2
antinodes = set()
for v in antennas.values():
    for pos in v:
        antinodes.add(pos)

for k, v in antennas.items():
    comb = itertools.combinations(v, 2)
    stack = list(comb)
    processed = set()
    while stack:
        a, b = stack.pop()
        if not (a, b) in processed:
            processed.add((a, b))
            for antinode in get_antinodes(a, b):
                if is_in_grid(*antinode):
                    antinodes.add(antinode)
                    for comb in itertools.combinations([a, b, antinode], 2):
                        stack.append(comb)

print(len(antinodes))
