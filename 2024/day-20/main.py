from functools import cache
import itertools
from os import getenv

import networkx as nx

UP, DOWN, LEFT, RIGHT = "^", "v", "<", ">"
DIRS = {LEFT: (0, -1), RIGHT: (0, 1), UP: (-1, 0), DOWN: (1, 0)}


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


def is_in_grid(i: int, j: int) -> bool:
    return 0 <= i < I and 0 <= j < J


def print_path(path):
    for i in range(I):
        for j in range(J):
            if (i, j) in path:
                print("O", end="")
            else:
                print(grid[i][j], end="")
        print()


def find_initial_dir():
    i, j = START
    for di, dj in DIRS.values():
        ni, nj = i + di, j + dj
        if is_in_grid(ni, nj) and grid[ni][nj] != "#":
            return (di, dj)
    raise ValueError("Cannot find initial direction!")


def trace_path():
    i, j = START
    path = [START]
    di, dj = find_initial_dir()

    while (i, j) != END:
        ni, nj = i + di, j + dj
        if is_in_grid(ni, nj) and grid[ni][nj] != "#":
            path.append((ni, nj))
            i, j = ni, nj
            continue

        for di, dj in set(DIRS.values()) - {(di, dj), (-di, -dj)}:
            ni, nj = i + di, j + dj
            if is_in_grid(ni, nj) and grid[ni][nj] != "#":
                break
        else:
            raise ValueError("Cannot find next direction!")

    return path


def find_cheats():
    cheats = {}
    for a, b in itertools.combinations(path, 2):
        ai, aj = a
        bi, bj = b
        d = abs(ai - bi) + abs(aj - bj)
        if d >= 2 and d <= 20:
            cheats[(a, b)] = d
            cheats[(b, a)] = d
    return cheats


@cache
def get_distance(a, b):
    return nx.shortest_path_length(G, a, b)

def solve(cheats):
    res = 0
    for k, v in cheats.items():
        start, end = k
        d1 = get_distance(START, start)
        d2 = v
        d3 = get_distance(end, END)
        d = d1 + d2 + d3
        gain = length - d
        if gain >= 100:
            res += 1
    return res


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    grid = [line.strip() for line in f.readlines()]

I = len(grid)
J = len(grid[0])

START, END = find_start(), find_end()

path = trace_path()

G = nx.DiGraph()
for u, v in zip(path, path[1:]):
    G.add_edge(u, v)

assert list(nx.shortest_path(G, START, END)) == path
length = len(path)

all_cheats = find_cheats()
cheats = {c: v for c, v in all_cheats.items() if v == 2}

print(solve(cheats))
print(solve(all_cheats))
