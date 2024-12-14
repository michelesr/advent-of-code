from os import getenv
from collections import Counter
from math import prod
import re


def print_robots(robots):
    pos = Counter([r[0] for r in robots])
    for y in range(Y):
        for x in range(X):
            print(pos.get((x, y), "."), end="")
        print()


def count_robots_in_quadrants(robots):
    quadrants = [
        # top left
        [range(0, X // 2), range(0, Y // 2)],
        # top right
        [range(X // 2 + 1, X), range(0, Y // 2)],
        # bottom left
        [range(0, X // 2), range(Y // 2 + 1, Y)],
        # bottom right
        [range(X // 2 + 1, X), range(Y // 2 + 1, Y)],
    ]

    pos = Counter([r[0] for r in robots])
    res = [0, 0, 0, 0]
    for k, v in pos.items():
        x, y = k
        for n, q in enumerate(quadrants):
            if x in q[0] and y in q[1]:
                res[n] += v
    return res


def move(robots, seconds):
    t = seconds
    for n, robot in enumerate(robots):
        x, y = robot[0]
        vx, vy = robot[1]
        x = (x + (vx * t)) % X
        y = (y + (vy * t)) % Y
        robots[n][0] = (x, y)


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    lines = [line.strip() for line in f.readlines()]

X, Y = [int(n) for n in lines[0].split(" ")]
REGEX = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")

robots = []
for line in lines[1:]:
    r = re.match(REGEX, line)
    if not r:
        raise ValueError("Invalid input")
    g = r.groups()
    robots.append([(int(g[0]), int(g[1])), (int(g[2]), int(g[3]))])

# use this loop to find the tree in part 2 (press enter to print a tree)
# move(robots, 82)
# t = 82
# while True:
#     input()
#     print(t)
#     print()
#     print_robots(robots)
#     move(robots, 101)
#     t += 101

# part one
move(robots, 100)
print(prod(count_robots_in_quadrants(robots)))
