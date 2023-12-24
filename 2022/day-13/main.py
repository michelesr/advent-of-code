from functools import cmp_to_key
from enum import Enum


class Result(Enum):
    correct = 1
    incorrect = 0
    undefined = -1


def compare_root(a, b) -> int:
    r = compare(a, b)
    match r:
        case Result.undefined:
            raise ValueError("undefined comparison")
        case Result.correct:
            return -1
        case Result.incorrect:
            return 1


def compare(a, b) -> Result:
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return Result.correct
        elif a == b:
            return Result.undefined
        else:
            return Result.incorrect
    elif isinstance(a, list) and isinstance(b, int):
        b = [b]
        return compare(a, b)
    elif isinstance(a, int) and isinstance(b, list):
        a = [a]
        return compare(a, b)
    elif isinstance(a, list) and isinstance(b, list):
        m, n = len(a), len(b)
        for i in range(min(m, n)):
            r = compare(a[i], b[i])
            if r != Result.undefined:
                return r
        if m < n:
            return Result.correct
        elif m > n:
            return Result.incorrect
    return Result.undefined


key_func = cmp_to_key(compare_root)

with open("input", "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]

pairs = []
i = 0
while i < len(lines) - 1:
    pair = (eval(lines[i]), eval(lines[i + 1]))
    pairs.append(pair)
    i += 3


# part one
res = 0
for i in range(len(pairs)):
    a, b = pairs[i]
    r = compare(a, b)
    if r == Result.correct:
        res += i + 1
print(res)

# part two:
packets = [[[2]], [[6]]]
for pair in pairs:
    packets.append(pair[0])
    packets.append(pair[1])

res = list(sorted(packets, key=key_func))
res = (res.index([[2]]) + 1) * (res.index([[6]]) + 1)
print(res)
