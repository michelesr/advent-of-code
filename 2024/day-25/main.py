from os import getenv
from enum import Enum


def fits(lh, kh):
    return all(lh[i] + kh[i] <= 5 for i in range(len(lh)))


class State(Enum):
    NEW = 0
    KEY = 1
    LOCK = 2


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    lines = [line.strip() for line in f.readlines()]

keys, locks = [], []
key, lock = [], []
state = State.NEW

for line in lines:
    if line == "":
        if state == State.KEY:
            keys.append(key)
        elif state == State.LOCK:
            locks.append(lock)
        else:
            raise ValueError("Invalid state")
        state = State.NEW
    elif state == State.NEW:
        if line == 5 * "#":
            state = State.LOCK
            lock = [line]
        else:
            state = State.KEY
            key = [line]
    elif state == State.KEY:
        key.append(line)
    elif state == State.LOCK:
        lock.append(line)
else:
    if state == State.KEY:
        keys.append(key)
    elif state == State.LOCK:
        locks.append(lock)

lh, kh = [], []
for lock in locks:
    lock = zip(*lock[1:])
    lh.append([sum(1 for x in col if x == "#") for col in lock])
for key in keys:
    key = zip(*key[:-1])
    kh.append([sum(1 for x in col if x == "#") for col in key])

print(sum(1 for l in lh for k in kh if fits(l, k)))
