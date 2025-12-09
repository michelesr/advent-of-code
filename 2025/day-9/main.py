from functools import cache
from itertools import combinations
from os import getenv
from typing import cast

from shapely.geometry import Polygon

Tile = tuple[int, int]


@cache
def area(a: Tile, b: Tile) -> int:
    """Returns the area of the rectangle with 'a' and 'b' as opposite vertices"""
    a1, a2 = a
    b1, b2 = b
    return (abs(a1 - b1) + 1) * (abs(a2 - b2) + 1)


def max_area(tiles, path: Polygon | None = None) -> int:
    """Returns the max area that can be formed with the given tiles"""
    return max(
        area(a, b)
        for a, b in combinations(tiles, 2)
        if not path or check_rectangle(path, a, b)
    )


def check_rectangle(path: Polygon, a: Tile, c: Tile) -> bool:
    """Check if the rectangle is inside a valid area for part two"""
    # a b c d are the vertices sorted (a must be in the top edge)
    ai, aj = a
    ci, cj = c

    b = (ai, cj)
    d = (ci, aj)

    inner_path = Polygon([a, b, c, d])
    return path.contains(inner_path)


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    tiles = [
        cast(Tile, tuple(int(n) for n in line.strip().split(",")))
        for line in f.readlines()
    ]

# part one
print(max_area(tiles))

# part two, pass the Polygon obtained connecting all the tiles together
print(max_area(tiles, Polygon(tiles)))
