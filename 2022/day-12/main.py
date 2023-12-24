from typing import Optional


with open("input", "r") as file:
    grid = [line.strip("\n") for line in file.readlines()]


def get_value(letter: str) -> int:
    if letter.isupper():
        return ord({"S": "a", "E": "z"}[letter])
    else:
        return ord(letter)


def find_target(grid: list[str], target: str) -> list[tuple[int, int]]:
    res = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == target:
                res.append((i, j))
    return res


def find_end(grid: list[str]) -> tuple[int, int]:
    return find_target(grid, "E")[0]


def find_start(grid: list[str]) -> tuple[int, int]:
    return find_target(grid, "S")[0]


def find_paths(grid, i, j):
    res = []
    for a, b in (i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1):
        if a < 0 or a >= len(grid) or b < 0 or b >= len(grid[0]):
            continue
        if get_value(grid[a][b]) <= get_value(grid[i][j]) + 1:
            res.append((a, b))
    return res


def bfs(visit_complete, graph, current_node, end):
    global run
    print(f"Run #{run}")
    run += 1
    visit_complete.append(current_node)
    queue = []
    parents = {}
    queue.append(current_node)

    i = 0
    while queue:
        s = queue.pop(0)
        if s == end:
            while parents.get(s):
                s = parents[s]
                i += 1
            break
        for neighbour in graph[s]:
            if neighbour not in visit_complete:
                parents[neighbour] = s
                visit_complete.append(neighbour)
                queue.append(neighbour)
    return i


run = 0
start = find_start(grid)
end = find_end(grid)

graph = {}
for x in range(len(grid)):
    for y in range(len(grid[0])):
        graph[(x, y)] = find_paths(grid, x, y)

# part one
res = bfs([], graph, start, end)
print(f"Result -> {res}")

# part two (takes a while to compute)
targets = find_target(grid, "a")
res = [bfs([], graph, s, end) for s in targets]
res = set(res)
res.remove(0)
res = min(res)
print(f"Result -> {res}")
