from os import getenv

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    grid = [line.strip() for line in f.readlines()]


def part_one(grid):
    WORD = "XMAS"
    word_len = len(WORD)
    words = (WORD, WORD[::-1])

    count = 0

    # Search horizontally
    for row in grid:
        for i in range(len(row) - word_len + 1):
            if row[i : i + word_len] in words:
                count += 1

    # Search vertically
    for col in range(len(grid[0])):
        for i in range(len(grid) - word_len + 1):
            column = [grid[j][col] for j in range(i, i + word_len)]
            if "".join(column) in words:
                count += 1

    # Search diagonally (top-left to bottom-right)
    for row in range(len(grid) - word_len + 1):
        for col in range(len(grid[0]) - word_len + 1):
            diagonal = [grid[row + j][col + j] for j in range(word_len)]
            if "".join(diagonal) in words:
                count += 1

    # Search diagonally (bottom-left to top-right)
    for row in range(word_len - 1, len(grid)):
        for col in range(len(grid[0]) - word_len + 1):
            diagonal = [grid[row - j][col + j] for j in range(word_len)]
            if "".join(diagonal) in words:
                count += 1

    return count


def part_two(grid):
    WORD = "MAS"
    word_len = len(WORD)
    words = (WORD, WORD[::-1])
    count = 0

    for row in range(len(grid) - word_len + 1):
        for col in range(len(grid[0]) - word_len + 1):
            for word in words:
                if (
                    grid[row][col] == word[0]
                    and grid[row + 1][col + 1] == word[1]
                    and grid[row + 2][col + 2] == word[2]
                ) and (
                    (grid[row][col + 2] == word[0] and grid[row + 2][col] == word[2])
                    or (grid[row][col + 2] == word[2] and grid[row + 2][col] == word[0])
                ):
                    count += 1
    return count


print(part_one(grid))
print(part_two(grid))
