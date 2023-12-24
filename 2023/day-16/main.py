from sys import argv, setrecursionlimit

setrecursionlimit(10000)

# directions
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


def get_slash_next_pos(position: tuple[int, int, int]) -> tuple[int, int, int]:
    i, j, d = position
    if d == LEFT:
        return (i + 1, j, DOWN)
    if d == RIGHT:
        return (i - 1, j, UP)
    if d == UP:
        return (i, j + 1, RIGHT)
    if d == DOWN:
        return (i, j - 1, LEFT)
    raise ValueError(f"Invalid data {position}")


def get_backslash_next_pos(position: tuple[int, int, int]) -> tuple[int, int, int]:
    i, j, d = position
    if d == LEFT:
        return (i - 1, j, UP)
    if d == RIGHT:
        return (i + 1, j, DOWN)
    if d == UP:
        return (i, j - 1, LEFT)
    if d == DOWN:
        return (i, j + 1, RIGHT)
    raise ValueError(f"Invalid data {position}")


def get_regular_next_pos(position: tuple[int, int, int]) -> tuple[int, int, int]:
    i, j, d = position
    if d == LEFT:
        return (i, j - 1, d)
    if d == RIGHT:
        return (i, j + 1, d)
    if d == UP:
        return (i - 1, j, d)
    if d == DOWN:
        return (i + 1, j, d)
    raise ValueError(f"Invalid data {position}")


def move(
    position: tuple[int, int, int],
    visited: set[tuple[int, int, int]],
):
    i, j, d = position
    is_out = i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0])
    if position in visited or is_out:
        return
    visited.add(position)

    match grid[i][j]:
        case ".":
            move(get_regular_next_pos(position), visited)
        case "/":
            move(get_slash_next_pos(position), visited)
        case "\\":
            move(get_backslash_next_pos(position), visited)
        case "|":
            if d in [UP, DOWN]:
                move(get_regular_next_pos(position), visited)
            else:
                move((i - 1, j, UP), visited)
                move((i + 1, j, DOWN), visited)
        case "-":
            if d in [LEFT, RIGHT]:
                move(get_regular_next_pos(position), visited)
            else:
                move((i, j - 1, LEFT), visited)
                move((i, j + 1, RIGHT), visited)


filename = "./input"
if len(argv) >= 2:
    filename = argv[1]

with open(filename) as f:
    grid = [line.strip() for line in f.readlines()]


def score(i, j, d):
    visited = set()
    move((i, j, d), visited)
    visited = {(i, j) for i, j, _ in visited}
    return len(visited)


# part 1
print(score(0, 0, RIGHT))

# part 2
res = 0
for i in range(len(grid[0])):
    res = max(res, score(0, i, DOWN))
    res = max(res, score(len(grid) - 1, i, UP))
for i in range(len(grid)):
    res = max(res, score(i, 0, RIGHT))
    res = max(res, score(i, len(grid[0]) - 1, LEFT))
print(res)
