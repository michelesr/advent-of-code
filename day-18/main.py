from matplotlib.path import Path
from sys import argv

lines = [line.strip().split(" ") for line in open(argv[1])]
lines = [(x[0], int(x[1]), x[2].replace("(", "").replace(")", "")) for x in lines]

holes: list[tuple[int, int]] = [(0, 0)]
r, c = 0, 0

for line in lines:
    match line[0]:
        case "L":
            for i in range(c - 1, c - line[1] - 1, -1):
                c = i
                if (r, c) not in holes:
                    holes.append((r, c))
        case "R":
            for i in range(c + 1, c + line[1] + 1, 1):
                c = i
                if (r, c) not in holes:
                    holes.append((r, c))
        case "U":
            for i in range(r - 1, r - line[1] - 1, -1):
                r = i
                if (r, c) not in holes:
                    holes.append((r, c))
        case "D":
            for i in range(r + 1, r + line[1] + 1, 1):
                r = i
                if (r, c) not in holes:
                    holes.append((r, c))

print(len(holes))

MIN_I = min([x[0] for x in holes])
MAX_I = max([x[0] for x in holes])

MIN_J = min([x[1] for x in holes])
MAX_J = max([x[1] for x in holes])

p = Path(holes)

res = 0
for i in range(MIN_I, MAX_I + 1):
    for j in range(MIN_J, MAX_J + 1):
        if (i, j) in holes or p.contains_point((i, j)):
            res += 1

print(res)
