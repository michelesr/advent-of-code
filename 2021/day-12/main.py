from collections import Counter

with open("input", "r") as f:
    links = [(p[0], p[1].strip()) for p in map(lambda l: l.split('-'), f.readlines())]

graph = {}
for link in links:
    for node in link:
        if not node in graph:
            graph[node] = []
    graph[link[0]].append(link[1])
    graph[link[1]].append(link[0])

def trace(graph, start, end, path, paths, stop_f, continue_f):
    if stop_f(path):
        return
    path.append(start)
    if start == end:
        paths.append(path)
    else:
        for node in graph[start]:
            if continue_f(path, node):
                trace(graph, node, end, path.copy(), paths, stop_f, continue_f)

# part 1

paths = []
stop_f = lambda p: False
continue_f = lambda p, n : n.isupper() or n not in p
trace(graph, 'start', 'end', [], paths, stop_f, continue_f)

print(len(paths))

# part 2

def is_invalid(path):
    path = filter(lambda n: n.islower(), path)
    return Counter(Counter(path).values())[2] >= 2

paths = []
continue_f = lambda p, n: n != 'start' and (n.isupper() or Counter(p)[n] < 2)
trace(graph, 'start', 'end', [], paths, is_invalid, continue_f)

print(len(paths))
