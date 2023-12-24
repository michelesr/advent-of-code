from itertools import combinations
from copy import deepcopy, copy


def get_row(i):
    return grid[i]


def get_col(i):
    return [row[i] for row in grid]


def print_grid():
    for row in grid:
        print("".join(row))


def find_galaxies():
    res = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "#":
                res.append((i, j))
    return res


def expand():
    for i in reversed(EMPTY_ROWS):
        grid.insert(i, copy(grid[i]))
    for j in reversed(EMPTY_COLS):
        for row in grid:
            row.insert(j, row[j])


def distance(a, b):
    y1, x1 = a
    y2, x2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def distance2(a, b, multiplier=1000000):
    y1, x1 = a
    y2, x2 = b
    empty_rows = [i for i in EMPTY_ROWS if i in range(y1, y2)]
    step = 1
    if x2 < x1:
        step = -1
    empty_cols = [i for i in EMPTY_COLS if i in range(x1, x2, step)]

    dy = abs(y1 - y2) + (len(empty_rows) * (multiplier - 1))
    dx = abs(x1 - x2) + (len(empty_cols) * (multiplier - 1))
    return dy + dx


with open("./input") as f:
    grid = [list(line.strip()) for line in f.readlines()]

EMPTY_ROWS = [i for i in range(len(grid)) if "#" not in get_row(i)]
EMPTY_COLS = [i for i in range(len(grid[0])) if "#" not in get_col(i)]

old_grid = deepcopy(grid)

expand()
print(sum((distance(a, b) for a, b in combinations(find_galaxies(), 2))))

grid = old_grid
print(sum((distance2(a, b) for a, b in combinations(find_galaxies(), 2))))
