import re
from os import getenv

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    text = f.read()

factors = re.findall(r"mul\((\d+),(\d+)\)", text)
print(sum(int(a) * int(b) for a, b in factors))

enabled, res = True, 0
for match in re.findall(r"(do\(\)|don't\(\)|mul\((\d+),(\d+)\))", text):
    if match[0] == "do()":
        enabled = True
    elif match[0] == "don't()":
        enabled = False
    elif enabled:
        res += int(match[1]) * int(match[2])
print(res)
