from os import getenv
from functools import cache

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    grid = [line.strip() for line in f.readlines()]

ROWS = len(grid)
COLUMNS = len(grid[0])


def is_in_grid(i, j):
    return 0 <= i < ROWS and 0 <= j < COLUMNS


def part_one(grid, start):
    splits = 0
    stack = [start]
    visited = set()

    while stack:
        i, j = stack.pop()
        if (i, j) in visited:
            continue
        visited.add((i, j))
        if not is_in_grid(i, j):
            continue
        if grid[i][j] in (".", "S"):
            stack.append((i + 1, j))
        elif grid[i][j] == "^":
            splits += 1
            stack.append((i + 1, j - 1))
            stack.append((i + 1, j + 1))
        else:
            raise ValueError("Invalid data")
    return splits


def part_two(grid, start):
    @cache
    def count_timelines(i: int, j: int) -> int:
        if not is_in_grid(i, j):
            return 1
        if grid[i][j] in (".", "S"):
            return count_timelines(i + 1, j)
        if grid[i][j] == "^":
            return count_timelines(i + 1, j + 1) + count_timelines(i + 1, j - 1)
        else:
            raise ValueError("Invalid data")

    return count_timelines(*start)


start = (int(0), grid[0].index("S"))
print(part_one(grid, start))
print(part_two(grid, start))
