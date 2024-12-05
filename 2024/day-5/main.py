from os import getenv

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    section_two = False
    rules = []
    updates = []
    for line in f.readlines():
        if line == '\n':
            section_two = True
            continue
        if not section_two:
            parts = line.split('|')
            rules.append((int(parts[0]), int(parts[1])))
        else:
            updates.append([int(x) for x in line.split(',')])

def check_update(update: list[int]):
    for n, i in zip(update, range(len(updates))):
        rules_to_check = [r for r in rules if n in r]
        for r in rules_to_check:
            if n == r[0] and r[1] in update[:i] or n == r[1] and r[0] in update[i+1:]:
                return (update, n, i, r)
    return None

def is_good_update(update: list[int]) -> bool:
    return check_update(update) is None

def correct_update(update, n, i, r):
    before = n == r[0]
    del update[i]
    if before:
        index = update.index(r[1]) 
    else:
        index = update.index(r[0]) + 1
    update.insert(index, n)

good_updates = [u for u in updates if is_good_update(u)]
print(sum(u[(len(u) - 1) // 2] for u in good_updates))

bad_updates = [u for u in updates if not is_good_update(u)]

for u in bad_updates:
    while (res := check_update(u)) is not None:
        correct_update(*res)

print(sum(u[(len(u) - 1) // 2] for u in bad_updates))
