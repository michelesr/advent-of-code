from functools import cache
from os import getenv

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    graph = {parts[0]: parts[1].split(' ') for parts in [line.strip().split(': ') for line in f]}

def solve_part_one(graph) -> int:
    stack = ['you']
    paths = 0
    while stack:
        current = stack.pop()
        if current == 'out':
            paths += 1
            continue
        for child in graph[current]:
            stack.append(child)
    return paths

def solve_part_two(graph) -> int:
    @cache
    def count_valid_paths(current, found_dac=False, found_fft=False) -> int:
        if current == 'out':
            return int(found_dac and found_fft)
        elif current == 'dac':
            found_dac = True
        elif current == 'fft':
            found_fft = True
        return sum(count_valid_paths(child, found_dac=found_dac, found_fft=found_fft) for child in graph[current])
    return count_valid_paths('svr')

print(solve_part_one(graph))
print(solve_part_two(graph))
