from os import getenv
from copy import deepcopy

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    grid = [list(line.strip()) for line in f.readlines()]

I = len(grid)
J = len(grid[0])
UP, DOWN, LEFT, RIGHT = "^", "v", "<", ">"
DIRECTIONS = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}
start: tuple[int, int, str] | None = None


def is_in_grid(i, j):
    return 0 <= i < I and 0 <= j < J


def rotate(direction: str) -> str:
    return {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}[direction]


def check_grid(grid, start):
    i, j, d = start
    path = set()
    while is_in_grid(i, j):
        if (i, j, d) in path:
            return (path, True)
        path.add((i, j, d))

        # check obstacle
        di, dj = DIRECTIONS[d]

        while is_in_grid(i + di, j + dj) and grid[i + di][j + dj] == "#":
            d = rotate(d)
            di, dj = DIRECTIONS[d]

        i, j = i + di, j + dj
    return (path, False)


for i in range(I):
    for j in range(J):
        if grid[i][j] in DIRECTIONS.keys():
            start = (i, j, grid[i][j])

if start is None:
    raise ValueError("Cannot find start")

# part one
visited = {(i, j) for i, j, _ in check_grid(grid, start)[0]}
print(len(visited))

# part two
possible_obstacles = visited - {(start[0], start[1])}
res = 0
for i, j in possible_obstacles:
    new_grid = deepcopy(grid)
    new_grid[i][j] = "#"
    if check_grid(new_grid, start)[1]:
        res += 1

print(res)
