from os import getenv

import networkx as nx

LEFT, RIGHT, UP, DOWN = "<", ">", "^", "v"

DIRS: dict[str, tuple[int, int]] = {
    LEFT: (0, -1),
    RIGHT: (0, 1),
    UP: (-1, 0),
    DOWN: (1, 0),
}


def is_in_grid(x, y):
    return 0 <= x < X and 0 <= y < Y


def print_path(path: list[tuple[int, int]]):
    for y in range(Y):
        for x in range(X):
            if (y, x) in path:
                print("O", end="")
            else:
                print(grid[y][x], end="")
        print()
    print()


def get_intersections(grid) -> list[tuple[tuple[int, int], list[tuple[int, int]]]]:
    res: list[tuple[tuple[int, int], list[tuple[int, int]]]] = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != "#":
                ways = []
                for di, dj in DIRS.values():
                    ni, nj = i + di, j + dj
                    if is_in_grid(ni, nj) and grid[ni][nj] != "#":
                        ways.append((di, dj))
                if len(ways) > 2:
                    res.append(((i, j), ways))
    return res


def find_connections(
    grid: list[list[str]],
    node: tuple[tuple[int, int], list[tuple[int, int]]],
    nodes,
) -> list[tuple[tuple[int, int], int]]:
    start, directions = node
    si, sj = start
    res = []
    for di, dj in directions:
        found = False
        ni, nj = si + di, sj + dj
        cost = 1

        can_continue = True
        while not found and can_continue:
            while is_in_grid(ni, nj) and grid[ni][nj] != "#":
                if (ni, nj) in nodes:
                    found = True
                    break
                ni, nj = ni + di, nj + dj
                cost += 1
            if found:
                pos = ni, nj
                res.append((pos, cost))
                break

            # since we found a wall, lets step back
            ni, nj = ni - di, nj - dj

            # switch direction, ignore same and opposite
            for i, j in set(DIRS.values()) - {(di, dj), (-di, -dj)}:
                if (
                    is_in_grid(ni, nj)
                    and is_in_grid(ni + i, nj + j)
                    and grid[ni + i][nj + j] != "#"
                ):
                    di, dj = i, j
                    ni, nj = ni + di, nj + dj
                    can_continue = True
                    break
                can_continue = False
    return res


def print_grid(grid):
    for row in grid:
        print("".join(row))


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    coords = [tuple([int(n) for n in line.split(",")]) for line in f.readlines()]

# real input needs 71
X = int(getenv("AOC_SQUARE_SIZE", "7"))
Y = X

START, END = (0, 0), (X - 1, Y - 1)

# real input needs 1024
BYTES_TO_FALL = int(getenv("AOC_FALL_BYTES", "12"))

# print(coords)

grid = [
    ["#" if (j, i) in coords[:BYTES_TO_FALL] else "." for j in range(Y)]
    for i in range(X)
]


def solve():
    nodes_with_dir = get_intersections(grid)
    # add start and end nodes
    start_dirs = []
    si, sj = START
    for di, dj in (DIRS[DOWN], DIRS[RIGHT]):
        ni, nj = si + di, sj + dj
        if grid[ni][nj] != "#":
            start_dirs.append((di, dj))

    start = (START, start_dirs)
    end = (END, [])

    nodes_with_dir.insert(0, start)
    nodes_with_dir.append(end)

    nodes = [n[0] for n in nodes_with_dir]

    network = nx.Graph()
    for node in nodes_with_dir:
        for connection in find_connections(grid, node, nodes):
            network.add_edge(node[0], connection[0], weight=connection[1])

    return nx.shortest_path_length(network, START, END, weight="weight")


# part one
print(solve())

# part two: use pypy to speed up brute forcing!
coords = coords[BYTES_TO_FALL:]
for x, y in coords:
    grid[y][x] = "#"
    try:
        solve()
    except (nx.NodeNotFound, nx.NetworkXNoPath):
        print(f"{x},{y}")
        break
