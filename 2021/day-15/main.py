from os import getenv
import networkx as nx

UP, DOWN, LEFT, RIGHT = "^", "v", "<", ">"
DIRECTIONS = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}


def is_in_grid(i, j):
    return 0 <= i < I and 0 <= j < J


def wrap(n):
    return n if n <= 9 else n % 10 + 1


def solve(grid):
    START = (0, 0)
    END = (I - 1, J - 1)

    graph = nx.DiGraph()

    for i in range(I):
        for j in range(J):
            for di, dj in DIRECTIONS.values():
                ni, nj = i + di, j + dj
                u, v = (i, j), (ni, nj)
                if is_in_grid(ni, nj) and not graph.has_edge(u, v):
                    graph.add_edge(u, v, risk=grid[ni][nj])

    return nx.shortest_path_length(graph, START, END, weight="risk")


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    grid = [[int(x) for x in line.strip()] for line in f.readlines()]


I = len(grid)
J = len(grid[0])
print(solve(grid))

# expand cols
for i in range(I):
    for n in range(4):
        for j in range(J):
            grid[i].append(wrap(grid[i][j] + n + 1))

# expand rows
J = len(grid[0])
for n in range(4):
    for i in range(I):
        row = [wrap(grid[i][j] + n + 1) for j in range(J)]
        grid.append(row)

I = len(grid)
J = len(grid[0])
print(solve(grid))
