from matplotlib.path import Path


def find_start() -> tuple[int, int]:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                return i, j
    raise ValueError("Cannot find start")


with open("./input") as f:
    grid = [line.strip() for line in f.readlines()]

current = find_start()
# by looking at the puzzle input graphically, it can be determined that down
# (+1, 0) is a valid move
current = (current[0] + 1, current[1])
last_move = (1, 0)
steps = 1
pipe = grid[current[0]][current[1]]

points = []
while pipe != "S":
    points.append(current)
    if pipe == "|":
        current = (current[0] + last_move[0], current[1])
    elif pipe == "-":
        current = (current[0], current[1] + last_move[1])
    elif pipe == "7":
        if last_move == (0, 1):
            current = (current[0] + 1, current[1])
            last_move = (1, 0)
        elif last_move == (-1, 0):
            current = (current[0], current[1] - 1)
            last_move = (0, -1)
    elif pipe == "J":
        if last_move == (1, 0):
            current = (current[0], current[1] - 1)
            last_move = (0, -1)
        elif last_move == (0, 1):
            current = (current[0] - 1, current[1])
            last_move = (-1, 0)
    elif pipe == "L":
        if last_move == (1, 0):
            current = (current[0], current[1] + 1)
            last_move = (0, 1)
        elif last_move == (0, -1):
            current = (current[0] - 1, current[1])
            last_move = (-1, 0)
    elif pipe == "F":
        if last_move == (-1, 0):
            current = (current[0], current[1] + 1)
            last_move = (0, 1)
        elif last_move == (0, -1):
            current = (current[0] + 1, current[1])
            last_move = (1, 0)
    else:
        raise ValueError("Error")
    steps += 1
    pipe = grid[current[0]][current[1]]


print(steps // 2)

p = Path(points)
res = 0
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if (x, y) in points:
            continue
        if p.contains_point((x, y)):
            res += 1

print(res)
