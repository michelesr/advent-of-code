from sys import argv


def overlaps(a, b):
    return max(a[0][0], b[0][0]) <= min(a[1][0], b[1][0]) and max(
        a[0][1], b[0][1]
    ) <= min(a[1][1], b[1][1])


def is_supported_by(a, b):
    return b[0][2] == a[1][2] + 1 and overlaps(a, b)


def can_disintegrate(i) -> bool:
    for j in supports_map[i]:
        if len(is_supported_map[j]) == 1:
            return False
    return True


with open(argv[1]) as f:
    lines = [line.strip() for line in f.readlines()]

bricks = []
for line in lines:
    parts = line.split("~")
    a, b = parts[0], parts[1]
    a = [int(x) for x in a.split(",")]
    b = [int(x) for x in b.split(",")]
    bricks.append((a, b))

# sort by height
bricks.sort(key=lambda x: x[0][2])

# the 1st block is already on the ground, so start from the 2nd
for i in range(1, len(bricks)):
    max_z = 1
    dz = bricks[i][1][2] - bricks[i][0][2]
    for j in range(i - 1, -1, -1):
        if overlaps(bricks[i], bricks[j]):
            max_z = max(max_z, bricks[j][1][2] + 1)
    bricks[i][0][2] = max_z
    bricks[i][1][2] = max_z + dz

bricks.sort(key=lambda x: x[0][2])

is_supported_map = {i: set() for i in range(len(bricks))}
supports_map = {i: set() for i in range(len(bricks))}

for i in range(1, len(bricks)):
    for j in range(i - 1, -1, -1):
        if is_supported_by(bricks[j], bricks[i]):
            is_supported_map[i].add(j)
            supports_map[j].add(i)

res = [can_disintegrate(i) for i in range(len(bricks))]
print(len([x for x in res if x]))
