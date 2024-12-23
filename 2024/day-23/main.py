from os import getenv
from itertools import combinations
import networkx as nx

def are_interconnected(nodes):
    for a, b in combinations(nodes, 2):
        if not G.has_edge(a, b):
            return False
    return True

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    connections = [line.strip().split('-') for line in f.readlines()]

G = nx.Graph()
for a, b in connections:
    G.add_edge(a, b)

# find possible combinations by concatenating sources with destinations
cs = {tuple(sorted([node] + list(G[node]))) for node in G.nodes()}

# find sets of 3 nodes that are interconnected
ts = set()
for s in cs:
    for comb in combinations(s, 3):
        if are_interconnected(comb) and [x for x in comb if x.startswith('t')]:
            ts.add(comb)

# part 1
print(len(ts))

# part 2
cl = list(nx.algorithms.find_cliques(G))
l = [len(x) for x in cl]
max_l = max(l)
res = cl[l.index(max_l)]
print(','.join(sorted(res)))
