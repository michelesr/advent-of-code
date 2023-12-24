from functools import reduce
import operator

MAX_CUBES = {"red": 12, "green": 13, "blue": 14}

with open("./input") as f:
    lines = f.readlines()


def game_is_valid(sets):
    for s in sets:
        for color, num in s.items():
            if num > MAX_CUBES[color]:
                return False
    return True


def get_game_cube_power(sets):
    max = {"red": 0, "green": 0, "blue": 0}
    for s in sets:
        for color, num in s.items():
            if num > max[color]:
                max[color] = num
    return reduce(operator.mul, max.values())


games = []
for line in lines:
    parts = line.split(":")
    id = int(parts[0].split(" ")[1])
    sets = []
    for game in parts[1].split(";"):
        d = {}
        for cube in game.split(","):
            cube = cube.split(" ")[1:]
            d[cube[1].strip()] = int(cube[0])
        sets.append(d)
    games.append((id, sets))

valid_games = [g for g in games if game_is_valid(g[1])]
valid_games_ids = [g[0] for g in valid_games]
print(sum(valid_games_ids))
print(sum([get_game_cube_power(g[1]) for g in games]))
