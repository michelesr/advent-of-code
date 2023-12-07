from functools import reduce
from operator import mul


def count_ways_to_win_race(max_time, max_distance):
    res = 0
    for j in range(max_time):
        speed = j
        t = max_time - j
        dist = speed * t
        if dist > max_distance:
            res += 1
    return res


with open("./input") as f:
    lines = f.readlines()
    times = [int(x) for x in lines[0].split()[1:]]
    distances = [int(x) for x in lines[1].split()[1:]]

# part one
wins = []
for i in range(len(times)):
    max_time, max_distance = times[i], distances[i]
    res = 0
    wins.append(count_ways_to_win_race(max_time, max_distance))

print(reduce(mul, wins, 1))

# part two
max_time = int("".join([str(t) for t in times]))
max_distance = int("".join([str(d) for d in distances]))

print(count_ways_to_win_race(max_time, max_distance))
