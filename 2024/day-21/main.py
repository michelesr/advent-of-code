from functools import cache
import itertools
from os import getenv

import networkx as nx

UP, DOWN, LEFT, RIGHT = "^", "v", "<", ">"
DIRS = {LEFT: (0, -1), RIGHT: (0, 1), UP: (-1, 0), DOWN: (1, 0)}
IDIRS = {v: k for k, v in DIRS.items()}


class Keypad:
    def __init__(self, keys):
        self.keys = keys
        self.G = self.make_graph()

    def make_graph(self):
        graph = nx.Graph()
        positions = [
            (i, j) for i in range(len(self.keys)) for j in range(len(self.keys[0]))
        ]
        positions.remove(self.get_position(" "))
        for a, b in itertools.combinations(positions, 2):
            if distance(a, b) == 1:
                graph.add_edge(a, b)
        return graph

    @cache
    def get_position(self, key):
        for i, row in enumerate(self.keys):
            if key in row:
                return i, row.index(key)
        raise ValueError(f"Key {key} not in keypad!")

    @cache
    def get_all_possible_paths(self, keycode):
        start = self.get_position("A")
        res = []
        stack = [((keycode), start, [])]
        while stack:
            keycode, start, pressed_keys = stack.pop()
            if len(keycode) == 0:
                res.append("".join(pressed_keys))
                continue
            end = self.get_position(keycode[0])
            paths = self.all_shortest_paths(start, end)
            paths = list(paths)
            for path in paths:
                dirs = self.get_path_directions(path)
                keys = pressed_keys + [IDIRS[d] for d in dirs] + ["A"]
                next = (keycode[1:], end, keys)
                stack.append(next)
        return tuple(res)

    @cache
    def shortest_path(self, start, end):
        return tuple(nx.shortest_path(self.G, start, end))

    @cache
    def all_shortest_paths(self, start, end):
        return tuple(nx.all_shortest_paths(self.G, start, end))

    def get_path_directions(self, path):
        return [get_movement_direction(a, b) for a, b in zip(path, path[1:])]


@cache
def get_movement_direction(a, b):
    ai, aj = a
    if distance(a, b) != 1:
        raise ValueError("Keys are not close")
    for di, dj in DIRS.values():
        ni, nj = ai + di, aj + dj
        if (ni, nj) == b:
            return (di, dj)
    raise ValueError("Direction not found!")


@cache
def distance(a, b):
    ai, aj = a
    bi, bj = b
    return abs(ai - bi) + abs(aj - bj)


def solve(code, n=2):
    return min(walk(path, n) for path in k1.get_all_possible_paths(code))


def get_result(codes, cutoff):
    res = 0
    for code in codes:
        l = solve(code, n=cutoff)
        n = get_numeric_part(code)
        res += l * n
    return res


def get_numeric_part(code):
    return int(code[:-1])


@cache
def find_cost(a, b, n):
    if n == 1:
        return len(k2.shortest_path(a, b))
    else:
        cost = float("inf")
        for path in k2.all_shortest_paths(a, b):
            start = k2.get_position("A")
            path_cost = 0
            for direction in [
                get_movement_direction(s, e) for s, e in zip(path, path[1:])
            ]:
                end = k2.get_position(IDIRS[direction])
                path_cost += find_cost(start, end, n - 1)
                start = end
            # the cost to activate the button once reached
            path_cost += find_cost(start, k2.get_position("A"), n - 1)
            cost = min(cost, path_cost)
        # this will raise error if cost is not set properly
        return int(cost)


def walk(keycode, n):
    start = k2.get_position("A")
    total_cost = 0
    for key in keycode:
        end = k2.get_position(key)
        total_cost += find_cost(start, end, n)
        start = end
    return total_cost


k1 = Keypad(("789", "456", "123", " 0A"))
k2 = Keypad((" ^A", "<v>"))

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    codes = [line.strip() for line in f.readlines()]

# part one
print(get_result(codes, cutoff=2))

# part two
print(get_result(codes, cutoff=25))
