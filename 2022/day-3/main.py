from functools import reduce

with open("input", "r") as f:
    items = [line.replace("\n", "") for line in f.readlines()]


def get_item_priority(letter: str):
    if letter.islower():
        return ord(letter) - 96
    elif letter.isupper():
        return ord(letter) - 38
    else:
        raise ValueError


def process(sack: list[str]) -> int:
    res = 0
    dups = []
    for item in sack[0]:
        if item not in dups and sack[1].find(item) >= 0:
            dups.append(item)
            res += get_item_priority(item)
    return res


# part one
part_one_items = list(map(lambda x: [x[0 : (len(x) // 2)], x[len(x) // 2 :]], items))
s = reduce(lambda res, sack: res + process(sack), part_one_items, 0)
print(s)

# part two
res = i = 0
n = len(items)

while i < len(items) - 2:
    for item in items[i]:
        if item in items[i + 1] and item in items[i + 2]:
            res += get_item_priority(item)
            break
    i += 3
print(res)
