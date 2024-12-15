from os import getenv
from copy import deepcopy

LEFT = "<"
RIGHT = ">"
UP = "^"
DOWN = "v"

DIRECTIONS = {LEFT: (0, -1), RIGHT: (0, 1), UP: (-1, 0), DOWN: (1, 0)}


def find_start(grid):
    for i in range(I):
        for j in range(J):
            if grid[i][j] == "@":
                return (i, j)
    raise ValueError("No start")


def print_grid(grid):
    for row in grid:
        print("".join(row))


def scale_grid(grid):
    grid = [
        "".join(row)
        .replace("#", "##")
        .replace("O", "[]")
        .replace(".", "..")
        .replace("@", "@.")
        for row in grid
    ]
    return [list(line) for line in grid]


def move_box(grid, start, direction, commit=False):
    i, j = start
    a, b = (i, j), (i, j + 1)

    di, dj = DIRECTIONS[direction]

    if direction == LEFT:
        spots = [a]
    elif direction == RIGHT:
        spots = [b]
    else:
        spots = [a, b]

    can_move = True
    for spot in spots:
        i, j = spot
        ni, nj = i + di, j + dj
        match grid[ni][nj]:
            case "#":
                return False
            case ".":
                can_move = can_move and True
            case "[" | "]":
                can_move = can_move and move_box(
                    grid, get_box_coords(grid, (ni, nj))[0], direction, commit
                )
            case _:
                raise ValueError("Invalid spot")

    if can_move and commit:
        i, j = a
        old_a = grid[i][j]

        i, j = b
        old_b = grid[i][j]

        for i, j in (a, b):
            grid[i][j] = "."

        i, j = a
        ni, nj = i + di, j + dj
        grid[ni][nj] = old_a

        i, j = b
        ni, nj = i + di, j + dj
        grid[ni][nj] = old_b

    return can_move


def get_box_coords(grid, pos):
    i, j = pos
    match grid[i][j]:
        case "[":
            a, b = (i, j), (i, j + 1)
        case "]":
            a, b = (i, j - 1), (i, j)
        case _:
            raise ValueError("Invalid box")
    return a, b


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    lines = [line.strip() for line in f.readlines()]

grid = []
for line in lines:
    if line.strip() == "":
        break
    grid.append(list(line.strip()))

I = len(grid)
J = len(grid[0])

i = lines.index("") + 1

directions = []
for line in lines[i:]:
    directions += list(line)

orig_grid = deepcopy(grid)

i, j = find_start(grid)

for direction in directions:
    di, dj = DIRECTIONS[direction]
    ni, nj = i + di, j + dj
    match grid[ni][nj]:
        case "#":
            pass
        case "O":
            # check first
            nni, nnj = ni + di, nj + dj
            while grid[nni][nnj] == "O":
                nni, nnj = nni + di, nnj + dj
            if grid[nni][nnj] != ".":
                continue

            grid[i][j] = "."
            grid[ni][nj] = "@"
            nni, nnj = ni + di, nj + dj
            while grid[nni][nnj] not in (".", "#"):
                grid[nni][nnj] = "O"
                nni, nnj = nni + di, nnj + dj
            if grid[nni][nnj] == ".":
                grid[nni][nnj] = "O"
            i, j = i + di, j + dj
        case _:
            grid[i][j] = "."
            grid[ni][nj] = "@"
            i, j = ni, nj

res = 0
for i in range(I):
    for j in range(J):
        if grid[i][j] == "O":
            res += 100 * i + j
print(res)

grid = scale_grid(orig_grid)

I = len(grid)
J = len(grid[0])

i, j = find_start(grid)
for direction in directions:
    di, dj = DIRECTIONS[direction]
    ni, nj = i + di, j + dj
    match grid[ni][nj]:
        case "#":
            pass
        case "[" | "]":
            start = get_box_coords(grid, (ni, nj))[0]
            if move_box(grid, start, direction):
                move_box(grid, start, direction, commit=True)
                grid[i][j] = "."
                grid[ni][nj] = "@"
                i, j = i + di, j + dj
        case _:
            grid[i][j] = "."
            grid[ni][nj] = "@"
            i, j = ni, nj

res = 0
for i in range(I):
    for j in range(J):
        if grid[i][j] == "[":
            a, b = get_box_coords(grid, (i, j))
            ai, aj = a
            bi, bj = b
            res += min(ai, bi) * 100 + min(aj, bj)

print(res)
