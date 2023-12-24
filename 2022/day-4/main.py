from functools import reduce


def range_strtoi(item):
    return (int(item[0]), int(item[1]))


def get_sets(item):
    a = set(range(item[0][0], item[0][1] + 1))
    b = set(range(item[1][0], item[1][1] + 1))
    return (a, b)


def is_subset(a, b):
    return a.issubset(b) or b.issubset(a)


def is_overlap(a, b):
    return bool(a.intersection(b))


with open("input", "r") as f:
    items = [line.split(",") for line in f.readlines()]

items = tuple(((item[0], item[1].replace("\n", "")) for item in items))
items = tuple(
    ((tuple(item[0].split("-")), tuple(item[1].split("-"))) for item in items)
)
items = tuple((((range_strtoi(item[0]), range_strtoi(item[1])) for item in items)))
items = tuple(((get_sets(item)) for item in items))

# part one
res = reduce(lambda count, item: count + int(is_subset(*item)), items, 0)
print(res)

# part two
res = reduce(lambda count, item: count + int(is_overlap(*item)), items, 0)
print(res)
