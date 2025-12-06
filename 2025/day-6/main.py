from os import getenv
from math import prod
from typing import Iterable


def transpose_matrix(matrix: list[str] | list[list[str]]) -> list[list[str]]:
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def process_nums(nums: Iterable[int], op: "str"):
    return {"+": sum, "*": prod}[op](nums)


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    lines = f.readlines()

# part one
nums = [line.strip().split() for line in lines]
nums = transpose_matrix(nums)

print(sum(process_nums(map(int, row[:-1]), row[-1]) for row in nums))

# part two
operators = lines.pop().split()
operators.reverse()

lines = transpose_matrix(lines)[:-1]

res = 0
nums = []
current_op = operators.pop()

for column in lines:
    if column == [" "] * len(column):
        res += process_nums(nums, current_op)
        nums = []
        current_op = operators.pop()
        continue
    nums.append(int("".join(column)))

res += process_nums(nums, current_op)
print(res)
