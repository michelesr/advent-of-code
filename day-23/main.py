from sys import argv

DIRS: dict[str, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def get_intersections(grid) -> list[tuple[tuple[int, int], list[tuple[int, int]]]]:
    res: list[tuple[tuple[int, int], list[tuple[int, int]]]] = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != "#":
                ways = []
                for di, dj in DIRS.values():
                    ni, nj = i + di, j + dj
                    in_grid = 0 <= ni < len(grid) and 0 <= nj < len(grid[0])
                    if in_grid and grid[ni][nj] != "#":
                        ways.append((di, dj))
                if len(ways) > 2:
                    res.append(((i, j), ways))
    return res


def find_connections(
    grid: list[str], node: tuple[tuple[int, int], list[tuple[int, int]]], nodes
) -> list[tuple[int, int, int]]:
    start, directions = node
    si, sj = start
    res: list[tuple[int, int, int]] = []
    for di, dj in directions:
        found = False
        ni, nj = si + di, sj + dj
        steps = 1
        while not found:
            in_grid = 0 <= ni < len(grid) and 0 <= nj < len(grid[0])
            while in_grid and grid[ni][nj] != "#":
                # if (ni, nj) == (11, 21):
                #     __import__('pdb').set_trace()
                if (ni, nj) in nodes:
                    found = True
                    break
                ni, nj = ni + di, nj + dj
                steps += 1
                in_grid = 0 <= ni < len(grid) and 0 <= nj < len(grid[0])
            if found:
                res.append((ni, nj, steps))
                break
            ni, nj = ni - di, nj - dj
            # switch direction, ignore same and opposite
            for i, j in set(DIRS.values()) - {(di, dj), (-di, -dj)}:
                in_grid = 0 <= ni < len(grid) and 0 <= nj < len(grid[0])
                if in_grid and grid[ni + i][nj + j] != "#":
                    di, dj = i, j
                    ni, nj = ni + di, nj + dj
                    break
    return res


# plot the path in the grid
def gprint(paths, grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) in paths:
                print("O", end="")
            else:
                print(grid[i][j], end="")
        print()


# helper method to check if a is a subpath of b
def check(a, b):
    if len(b) < len(a):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


# slow but works for part 1
def search(grid: list[str]) -> list[int]:
    start: tuple[list[tuple[int, int]], tuple[int, int, int, int, int]] = (
        [(0, 1)],
        (0, 1, 0, -2, -2),
    )
    stack: list[tuple[list[tuple[int, int]], tuple[int, int, int, int, int]]] = [start]
    res = []

    while stack:
        old_paths, current = stack.pop()
        i, j, s, _, _ = current
        in_grid = 0 <= i < len(grid) and 0 <= j < len(grid[0])
        if not in_grid:
            continue
        x = grid[i][j]
        if x == "#":
            continue
        if i == len(grid) - 1 and j == len(grid[0]) - 2:
            res.append(s)
            continue
        if x in DIRS:
            paths = old_paths.copy()
            di, dj = DIRS[x]
            ni, nj = i + di, j + dj
            ns = s + 1
            if (ni, nj) not in paths:
                paths.append((ni, nj))
                stack.append((paths, (ni, nj, ns, di, dj)))
        else:
            for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                paths = old_paths.copy()
                di, dj = dir
                ni, nj = i + di, j + dj
                ns = s + 1
                if (ni, nj) not in paths:
                    paths.append((ni, nj))
                    stack.append((paths, (ni, nj, ns, di, dj)))
    return res


# good enough for part 2
def search2(network: dict[tuple[int, int], list[tuple[int, int, int]]]):
    start: tuple[tuple[int, int, int], list[tuple[int, int]]] = ((0, 1, 0), [(0, 1)])
    stack: list[tuple[tuple[int, int, int], list[tuple[int, int]]]] = [start]
    end_node = (len(grid) - 1, len(grid[0]) - 2)
    res = []

    while stack:
        current, old_visited = stack.pop()
        i, j, s = current
        if (i, j) == end_node:
            res.append(s)
        for node in network[(i, j)]:
            visited = old_visited.copy()
            ni, nj, ds = node
            ns = s + ds
            if (ni, nj) not in visited:
                visited.append((ni, nj))
                stack.append(((ni, nj, ns), visited))

    return res


with open(argv[1]) as f:
    grid = [line.strip() for line in f.readlines()]

res = search(grid)
print(max(res))

nodes_with_dir = get_intersections(grid)

# add start and end nodes
start: tuple[tuple[int, int], list[tuple[int, int]]] = ((0, 1), [(1, 0)])
end = ((len(grid) - 1, len(grid[0]) - 2), [])
nodes_with_dir.insert(0, start)
nodes_with_dir.append(end)

nodes = [n[0] for n in nodes_with_dir]

network = {n[0]: find_connections(grid, n, nodes) for n in nodes_with_dir}

res = search2(network)
print(max(res))
