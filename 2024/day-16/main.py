from collections import Counter
from os import getenv
from typing import cast

import networkx as nx

UP, DOWN, LEFT, RIGHT = "^", "v", "<", ">"
DIRS = {LEFT: (0, -1), RIGHT: (0, 1), UP: (-1, 0), DOWN: (1, 0)}
IDIRS = {(0, -1): LEFT, (0, 1): RIGHT, (-1, 0): UP, (1, 0): DOWN}


def turn_cost(a, b):
    if a == b:
        return 0
    elif rotate_clockwise(a) == b or rotate_counterclockwise(a) == b:
        return 1000
    elif rotate_clockwise(rotate_clockwise(a)) == b:
        return 2000
    else:
        raise ValueError("Invalid rotation")


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
    grid: list[str],
    node: tuple[tuple[int, int], list[tuple[int, int]]],
    nodes,
    start_dir: tuple[int, int],
) -> list[tuple[tuple[int, int], int]]:
    start, directions = node
    si, sj = start
    res = []
    for di, dj in directions:
        found = False
        ni, nj = si + di, sj + dj
        cost = 1

        if start_dir != (di, dj):
            cost += turn_cost(IDIRS[start_dir], IDIRS[(di, dj)])

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
                dir = None
                if pos != END:
                    dir = di, dj
                res.append(((pos, dir), cost))
                break

            # since we found a wall, lets step back
            ni, nj = ni - di, nj - dj

            # switch direction, ignore same and opposite
            for i, j in set(DIRS.values()) - {(di, dj), (-di, -dj)}:
                if is_in_grid(ni, nj) and grid[ni + i][nj + j] != "#":
                    cost += turn_cost(IDIRS[(di, dj)], IDIRS[(i, j)])
                    di, dj = i, j
                    ni, nj = ni + di, nj + dj
                    can_continue = True
                    break
                can_continue = False
    return res


def rotate_clockwise(direction):
    return {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}[direction]


def rotate_counterclockwise(direction):
    return {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}[direction]


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    grid = [line.strip() for line in f.readlines()]


def print_grid():
    for row in grid:
        print("".join(row))


def find_token(token):
    for i in range(I):
        for j in range(J):
            if grid[i][j] == token:
                return (i, j)
    raise ValueError("No start")


def find_start():
    return find_token(token="S")


def find_end():
    return find_token(token="E")


I = len(grid)
J = len(grid[0])


def is_in_grid(i: int, j: int) -> bool:
    return 0 <= i < I and 0 <= j < J


START, END = find_start(), find_end()

nodes_with_dir = get_intersections(grid)

start = (START, [DIRS[UP], DIRS[RIGHT]])
end = (END, [])

nodes_with_dir.insert(0, start)
nodes_with_dir.append(end)

nodes = [n[0] for n in nodes_with_dir]

network = nx.Graph()

for node in nodes_with_dir:
    pos, directions = node
    for dir in DIRS.values():
        for connection in find_connections(grid, node, nodes, dir):
            epos, edir = connection[0]
            weight = connection[1]
            network.add_edge((pos, dir), (epos, edir), weight=weight)

# part 1
path = nx.shortest_path(network, (START, DIRS[RIGHT]), (END, None), weight="weight")
print(nx.path_weight(network, path, weight="weight"))

# part 2
paths = nx.all_shortest_paths(
    network, (START, DIRS[RIGHT]), (END, None), weight="weight"
)

costs = {}
for path in paths:
    for u, v in zip(path, path[1:]):
        cost = cast(int, network[u][v]["weight"])
        # remove the turning cost
        while cost > 1000:
            cost -= 1000
        costs[(u[0], v[0])] = cost

counter = Counter(x[1] for x in costs.keys())
for k in counter.keys():
    counter[k] -= 1
print(sum(costs.values()) - sum(counter.values()) + 1)
