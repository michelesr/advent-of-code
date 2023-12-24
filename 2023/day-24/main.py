from sys import argv
from itertools import combinations
import sympy


class Hailstone:
    # basically a line, that can be defined by
    # the equation ax + by = c
    #
    # for the time t
    #
    # (X, Y) = (sx, sy) + t(vx, vy)
    #
    # x = sx + (t * vx), y = sy + (t * vy)
    #
    # t = (x - sx) / vx = (y - sy) / vy
    # vy(x - sx)  = vx(y - sy)
    #
    # (vy * x) - (vy * sx) = (vx * y) - (vx * sy)
    # (vy * x) - (vx * y) = (vy * sx) - (vx * sy)
    #
    # a = vy
    # b = -vx
    # c = (vy * sx) - (vx * sy)

    def __init__(self, sx, sy, sz, vx, vy, vz):
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.vx = vx
        self.vy = vy
        self.vz = vz

        self.a = vy
        self.b = -vx
        self.c = (vy * sx) - (vx * sy)

    def __repr__(self) -> str:
        return f"Hailstone({self.a}, {self.b}, {self.c})"

    def is_parallel(self, hs: "Hailstone") -> bool:
        # a1 / b1 == a2 / b2 -> a1 * b2 == a2 * b1
        return self.a * hs.b == hs.a * self.b

    def get_intersection(self, hs: "Hailstone") -> tuple[int, int]:
        # the formula above is the solution of
        # a1x + b1y = c1, a2x + b2y = c2
        # for x and y

        # easily solvable with cramer's rule
        # https://byjus.com/maths/cramers-rule/
        a1, b1, c1 = self.a, self.b, self.c
        a2, b2, c2 = hs.a, hs.b, hs.c
        return (
            (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1),
            (c2 * a1 - c1 * a2) / (a1 * b2 - a2 * b1),
        )

    def is_future(self, x) -> bool:
        # we want t > 0
        # t = (x - sx) / vx = (y - sy) / vy
        # if / 0 > 0 then * 0 is too > 0
        return (x - self.sx) * self.vx > 0


with open(argv[1]) as f:
    hailstones = [
        Hailstone(*[int(x) for x in line.strip().replace("@", ",").split(",")])
        for line in f.readlines()
    ]

# test area must must be passed as cli arg
test_min, test_max = int(argv[2]), int(argv[3])

res = 0
for a, b in combinations(hailstones, 2):
    if a.is_parallel(b):
        continue
    else:
        x, y = a.get_intersection(b)
        in_range = test_min <= x <= test_max and test_min <= y <= test_max
        if in_range and a.is_future(x) and b.is_future(x):
            res += 1
print(res)

# the idea for part two is to create a linear algebra system that can be resolved by a library
# so 
# let xr, yr, zr, vxr, vyr, vzr be the position and velocity of the rock
# let xh, yh, zh, vxh, vyh, vzh be the position and velocity of the hs
# for each coordinate we want:
# xr + t * (vxr) = xh + t * (vxh)
# (t * vxr) - (t * vxh) = xh - xr
# t * (vxr - vxh) = xh - xr
# t = (xh - xr) / (vxr - vxh)
# and this must be true for y and z so:
# t = (yh - yr) / (vyr - vyh)
# t = (zh - zr) / (vzr - vzh)
# and thus we want 
# (xh - xr) / (vxr - vxh) = (yh - yr) / (vyr - vyh)
# (yh - yr) / (vyr - vyh) = (zh - zr) / (vzr - vzh)
# and so
# (xh - xr) * (vyr - vyh) - (yh - yr) * (vxr - vxh) = 0
# (yh - yr) * (vzr - vzh) - (zh - zr) * (vyr - vyh) = 0

xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr, yr, zr, vxr, vyr, vzr")
equations = []
for hs in hailstones:
    xh, yh, zh, vxh, vyh, vzh = hs.sx, hs.sy, hs.sz, hs.vx, hs.vy, hs.vz
    equations.append((xh - xr) * (vyr - vyh) - (yh - yr) * (vxr - vxh))
    equations.append((yh - yr) * (vzr - vzh) - (zh - zr) * (vyr - vyh))

solutions = sympy.solve(equations)[0]
x, y, z = solutions[xr], solutions[yr], solutions[zr]
print(x + y + z)
