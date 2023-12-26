from sys import argv
from itertools import combinations
import networkx

with open(argv[1]) as f:
    network = {
        parts[0]: parts[1].split(" ")
        for parts in [line.strip().split(": ") for line in f.readlines()]
    }

graph = networkx.Graph()
for k, v in network.items():
    for x in v:
        graph.add_edge(k, x, capacity=1)

partition = None
for a, b in combinations(network.keys(), 2):
    n, partition = networkx.flow.minimum_cut(graph, a, b)
    if n == 3:
        break

if partition:
    print(len(partition[0]) * len(partition[1]))
