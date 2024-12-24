from os import getenv
from itertools import combinations
from functools import cache
from typing import cast


class Graph:
    def __init__(self):
        self.edges: set[tuple[str, str]] = set()

    def add_edge(self, a: str, b: str):
        self.edges.add(cast(tuple[str, str], tuple(sorted([a, b]))))
        self.__getitem__.cache_clear()
        self.nodes.cache_clear()

    @cache
    def __getitem__(self, item):
        edges = [e for e in self.edges if item in e]
        res = []
        for e in edges:
            res.append((set(e) - {item}).pop())
        return list(sorted(res))

    @cache
    def nodes(self):
        res = set()
        for a, b in self.edges:
            res.add(a)
            res.add(b)
        return res

    def has_edge(self, a: str, b: str):
        return b in self[a]

    def maximal_cliques(self):
        return self._bron_kerbosch(set(), set(self.nodes()), set())

    # https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    def _bron_kerbosch(self, r: set, p: set, x: set, res=None):
        if res is None:
            res = []
        if len(p) == len(x) == 0:
            res.append(set(r))
        for v in p.copy():
            self._bron_kerbosch(
                r.union({v}),
                p.intersection(set(self[v])),
                x.intersection(set(self[v])),
                res,
            )
            p.remove(v)
            x.add(v)
        return res


def are_interconnected(nodes):
    for a, b in combinations(nodes, 2):
        if not G.has_edge(a, b):
            return False
    return True


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    connections = [line.strip().split("-") for line in f.readlines()]

G = Graph()
for a, b in connections:
    G.add_edge(a, b)

# find possible combinations by concatenating sources with destinations
cs = {tuple(sorted([node] + list(G[node]))) for node in G.nodes()}

# find sets of 3 nodes that are interconnected
ts = set()
for s in cs:
    for comb in combinations(s, 3):
        if are_interconnected(comb) and [x for x in comb if x.startswith("t")]:
            ts.add(comb)

# part 1
print(len(ts))

# part 2
cl = G.maximal_cliques()
l = [len(x) for x in cl]
max_l = max(l)
res = cl[l.index(max_l)]
print(",".join(sorted(res)))
