from sys import argv
from collections import deque


def find_start(grid: list[list[str]]) -> tuple[int, int]:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                return (i, j)
    return (-1, -1)


def visit(
    start: tuple[int, int], grid: list[list[str]], max_steps: int
) -> set[tuple[int, int]]:
    q = deque()
    q.append((start[0], start[1], 0))
    visited = set()
    res = set()
    while len(q) > 0:
        x = q.popleft()
        i, j, n = x
        if n == max_steps:
            res.add((i, j))
        else:
            if x in visited:
                continue
            visited.add(x)
            for a, b in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + a, j + b
                # wrap ni, nj for the infinite grid
                wni = ni % width
                wnj = nj % width
                if grid[wni][wnj] != "#":
                    q.append((ni, nj, n + 1))
    return res


with open(argv[1]) as f:
    grid = [list(line.strip()) for line in f.readlines()]

width = len(grid[0])

start = find_start(grid)
res = visit(start, grid, 64)

print(len(res))

# let W be the width of the grid (that has to be squared)
assert len(grid) == len(grid[0])

# there should be a growth pattern that repeats with a period of W
# so that for each n < W exists a quadratic function f(x) that yields
# the problem result for a number of steps N = n + xW

# the number of steps N
steps = 26501365

# n is the remainder of steps / width
remainder = steps % width

# calculate 3 points, so f(0), f(1), f(2)

# x = n
v1 = len(visit(start, grid, remainder))

# x = n + W
v2 = len(visit(start, grid, remainder + width))

# x = n + 2W
v3 = len(visit(start, grid, remainder + 2 * width))

# Rule for making a quadratic equation from three points for 0, 1 and 2.
a = (v1 - 2 * v2 + v3) // 2
b = (-3 * v1 + 4 * v2 - v3) // 2
c = v1

# N = n + xW
x = steps // width
assert steps == remainder + (x * width)

# result is f(x)
result = (a * x * x) + (b * x) + c

print(result)
