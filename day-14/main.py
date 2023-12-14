from sys import argv


def transpose(matrix):
    res = [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]
    return tuple(["".join(row) for row in res])


def shift(line, reverse=True):
    parts = [sorted(list(part), reverse=reverse) for part in line.split("#")]
    parts = ["".join(part) for part in parts]
    return "#".join(parts)


def score(line):
    line = list(reversed(line))
    return sum([i + 1 for i in range(len(line)) if line[i] == "O"])


def gshift(grid, reverse=True):
    return tuple((shift(line, reverse) for line in grid))


def cycle(grid):
    grid = transpose(grid)
    grid = gshift(grid)
    grid = transpose(grid)
    grid = gshift(grid)
    grid = transpose(grid)
    grid = gshift(grid, False)
    grid = transpose(grid)
    grid = gshift(grid, False)
    return grid


def gprint(grid):
    for line in grid:
        print(line)


filename = "./input"
if len(argv) >= 2:
    filename = argv[1]

with open(filename) as f:
    grid = tuple([line.strip() for line in f.readlines()])

# part one
print(sum([score(line) for line in gshift(transpose(grid))]))

# part two
cache = {}
capture = False
captured = []
i = 0
while True:
    if grid not in cache:
        cache[grid] = 1
    elif cache[grid] == 1 and not capture:
        capture = True
        cache[grid] = 2
    elif cache[grid] == 2:
        break
    if capture:
        captured.append(sum([score(line) for line in transpose(grid)]))
    grid = cycle(grid)
    i += 1

period = len(captured)
start = i - period
print(captured[(1000000000 - start) % period])
