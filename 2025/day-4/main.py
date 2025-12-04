from os import getenv

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    grid = [list(line.strip()) for line in f.readlines()]

DIRS = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
ROWS, COLUMNS = len(grid), len(grid[0])


def is_in_grid(i, j):
    return 0 <= i < ROWS and 0 <= j < COLUMNS


def print_grid(grid):
    for row in grid:
        print("".join(row))


def remove_paper(grid) -> int:

    # find paper to remove
    pos = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if grid[i][j] == "@":
                adj_papers = 0
                for si, sj in DIRS:
                    ni, nj = i + si, j + sj
                    if is_in_grid(ni, nj) and grid[ni][nj] == "@":
                        adj_papers += 1
                if adj_papers < 4:
                    pos.append((i, j))

    # remove the paper
    for i, j in pos:
        grid[i][j] = "."

    # return count
    return len(pos)


res = remove_paper(grid)
print(res)
while n := remove_paper(grid):
    res += n
print(res)
