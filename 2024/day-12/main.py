from os import getenv

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    grid = [list(line.strip()) for line in f.readlines()]

I = len(grid)
J = len(grid[0])


def is_in_grid(i: int, j: int) -> bool:
    return 0 <= i < I and 0 <= j < J


def get_area(region):
    return len(region)


def get_perimeter(region):
    res = 0
    for i, j in region:
        for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if not is_in_grid(ni, nj) or grid[i][j] != grid[ni][nj]:
                res += 1
    return res


def get_corners(region):
    res = 0
    for i, j in region:
        for a, b, c in [
            [(i - 1, j), (i, j - 1), (i - 1, j - 1)],
            [(i - 1, j), (i, j + 1), (i - 1, j + 1)],
            [(i + 1, j), (i, j - 1), (i + 1, j - 1)],
            [(i + 1, j), (i, j + 1), (i + 1, j + 1)],
        ]:
            if a in region and b in region and c not in region:
                res += 1

        for a, b in [
            [(i, j - 1), (i - 1, j)],
            [(i, j + 1), (i - 1, j)],
            [(i, j - 1), (i + 1, j)],
            [(i, j + 1), (i + 1, j)],
        ]:
            if a not in region and b not in region:
                res += 1

    return res


seen = set()
stack = [(i, j) for j in range(J) for i in range(I)]
regions = []
while stack:
    i, j = stack.pop()
    if (i, j) in seen:
        continue
    seen.add((i, j))
    siblings = [(i, j)]
    for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if is_in_grid(ni, nj) and grid[i][j] == grid[ni][nj]:
            stack.append((ni, nj))
            siblings.append((ni, nj))
    found = False
    for node in siblings:
        for region in regions:
            if node in region:
                found = region
                break
    if not found:
        regions.append(set(siblings))
    else:
        regions[regions.index(found)] = found.union(set(siblings))

print(sum(get_area(r) * get_perimeter(r) for r in regions))
print(sum(get_area(r) * get_corners(r) for r in regions))
