from os import getenv

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    grid = [[int(n) for n in list(line.strip())] for line in f.readlines()]

I = len(grid)
J = len(grid[0])


def is_in_grid(i: int, j: int) -> bool:
    return 0 <= i < I and 0 <= j < J


def print_path(path: list[tuple[int, int]]):
    for i in range(I):
        for j in range(J):
            if (i, j) in path:
                print(grid[i][j], end="")
            else:
                print(".", end="")
        print()
    print()


def get_path_score(start: tuple[int, int]) -> tuple[int, int]:
    stack = [(start, [])]
    peaks = set()
    res = 0
    while stack:
        current, visited = stack.pop()
        i, j = current
        if current not in visited:
            visited.append(current)
            val = grid[i][j]
            if val == 9:
                peaks.add(current)
                res += 1
            for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if is_in_grid(ni, nj):
                    n_val = grid[ni][nj]
                    if n_val - val == 1:
                        stack.append(((ni, nj), visited.copy()))
    return len(peaks), res


starts = sorted([(i, j) for j in range(J) for i in range(I) if grid[i][j] == 0])
scores = [get_path_score(start) for start in starts]
print(sum(s[0] for s in scores))
print(sum(s[1] for s in scores))
