from os import getenv

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    first, last = [s.strip().split("\n") for s in f.read().split("\n\n")]
    ranges = [(int(a), int(b) + 1) for a, b in [r.strip().split("-") for r in first]]
    ids = [int(n) for n in last]


def overlaps(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[0] <= a[1]


def merge(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0], max(a[1], b[1]))


# merge all the ranges
ranges.sort()
merged = [ranges[0]]
for r in ranges[1:]:
    if overlaps(merged[-1], r):
        merged[-1] = merge(merged[-1], r)
    else:
        merged.append(r)
ranges = merged

count = 0
for n in ids:
    for a, b in ranges:
        if a <= n <= b:
            count += 1
print(count)
print(sum(b - a for a, b in ranges))
