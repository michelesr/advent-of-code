from itertools import cycle
from math import lcm
import re

LEFT = 0
RIGHT = 1

with open("./input") as f:
    lines = f.readlines()

directions = lines[0].strip().split()[0]
directions = [{"L": LEFT, "R": RIGHT}[d] for d in directions]

nodes = {}
for line in lines[2:]:
    matches = re.findall(r"[A-Z0-9]{3}", line)
    nodes[matches[0]] = (matches[1], matches[2])

steps = 0
current = "AAA"

# part 1
for dir in cycle(directions):
    current = nodes[current][dir]
    steps += 1
    if current == "ZZZ":
        break
print(steps)

# part 2
steps_l = []
starting_nodes = [node for node in nodes if node.endswith("A")]

for node in starting_nodes:
    steps = 0
    for dir in cycle(directions):
        node = nodes[node][dir]
        steps += 1
        if node.endswith("Z"):
            break
    steps_l.append(steps)

print(lcm(*steps_l))
