from os import getenv
from copy import copy


def find_sublist(main_list, sub_list):
    for i in range(len(main_list)):
        if main_list[i : i + len(sub_list)] == sub_list:
            return i
    return -1


def has_gaps(blocks):
    found_free = False
    for i in range(len(blocks)):
        if blocks[i] == ".":
            found_free = True
        if found_free and blocks[i] != ".":
            return True
    return False


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    text = f.read().strip()
    is_free_space = False
    id_number = 0
    blocks = []

    for c in text:
        l = int(c)
        if is_free_space:
            data = "."
        else:
            data = str(id_number)
            id_number += 1
        for i in range(l):
            blocks.append(data)
        is_free_space = not is_free_space

old_blocks = copy(blocks)

current = -1
while has_gaps(blocks):
    last = blocks[current]
    if blocks[current] != ".":
        blocks[current] = "."
        i = blocks.index(".")
        blocks[i] = last
    current -= 1

res = 0
for i in range(len(blocks)):
    if blocks[i] == ".":
        break
    res += i * int(blocks[i])
print(res)

blocks = old_blocks
current = -1
L = len(blocks)
done = {"."}

while True:
    length, current = 0, -1
    try:
        while blocks[current] in done:
            current -= 1
        val = blocks[current]
        while blocks[current] == val:
            current -= 1
            length += 1
    except IndexError:
        break
    done.add(val)
    n = L + current + 1
    index = find_sublist(blocks, ["."] * length)
    if index != -1 and index < n:
        for i in range(index, index + length):
            blocks[i] = val
        for i in range(n, n + length):
            blocks[i] = "."

res = 0
for i in range(len(blocks)):
    if blocks[i] == ".":
        continue
    res += i * int(blocks[i])
print(res)
