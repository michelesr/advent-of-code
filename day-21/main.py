from sys import argv
from collections import deque

def find_start(grid: list[list[str]]) -> tuple[int, int]:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                return (i, j)
    return (-1, -1)

with open(argv[1]) as f:
    grid = [list(line.strip()) for line in f.readlines()]
width = len(grid[0])

def visit(start: tuple[int, int], grid: list[list[str]], max_steps: int) -> set[tuple[int, int]]: 
    q = deque()
    q.append((start[0], start[1], 0))
    visited = set()
    res = set()
    while len(q) > 0:
        x = q.popleft()
        i, j, n = x
        if n == max_steps:
            res.add((i,j))
        else:
            if x in visited:
                continue
            visited.add(x)
            for (a, b) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + a, j + b
                # wrap ni, nj for the infinite grid
                wni = ni % width
                wnj = nj % width
                if grid[wni][wnj] != '#':
                    q.append((ni, nj, n+1))
    return res


start = find_start(grid)
res = visit(start, grid, 64)

print(len(res))

steps = 26501365
remainder = steps % width

assert len(grid[0]) == len(grid)

v1 = len(visit(start, grid, remainder))
v2 = len(visit(start, grid, remainder + width))
v3 = len(visit(start, grid, remainder + 2 * width))

# print(v1, v2, v3)

# Rule for making a quadratic equation from three points for 0, 1 and 2.
a = (v1 - 2 * v2 + v3) // 2
b = (-3 * v1 + 4 * v2 - v3) // 2
c = v1
n = steps // width

# print(f"Quadratic Equation is {a} n^2 + {b} n + {c}, with n = {n}")
result = (a * n * n) + (b * n) + c
print(result)
