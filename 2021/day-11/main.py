with open('input', 'r') as f:
    data = [list(a) for a in [b.strip() for b in f.readlines()]]

DAYS = 100
data = list(map(lambda x: list(map(int, x)), data))
I, J = range(len(data)), range(len(data[0]))

MAX_I, MAX_J = len(data) - 1, len(data[0]) - 1
def get_adjacent(i, j):
    res = []
    # N
    if i > 0:
        res.append((i - 1, j))
    # S
    if i < MAX_I:
        res.append((i + 1, j))
    # E
    if j > 0:
        res.append((i, j - 1))
    # W
    if j < MAX_J:
        res.append((i, j + 1))
    # NE
    if i > 0 and j > 0:
        res.append((i - 1, j - 1))
    # NW
    if i > 0 and j < MAX_J:
        res.append((i - 1, j + 1))
    # SE
    if i < MAX_I and j > 0:
        res.append((i + 1, j - 1))
    # SW
    if i < MAX_I and j < MAX_J:
        res.append((i + 1, j + 1))
    return res

def reset(data, flashed):
    for i in I:
        for j in J:
            if (i, j) in flashed:
                data[i][j] = 0

def increase_single(data, i, j):
    data[i][j] += 1

def increase(data):
    for i in I:
        for j in J:
            increase_single(data, i, j)

def check_flash_single(data, i, j, flashed, count):
    if data[i][j] > 9 and (i, j) not in flashed:
        flash(data, i, j, flashed, count)

def check_flash(data, flashed, count):
    for i in I:
        for j in J:
            check_flash_single(data, i, j, flashed, count)

def flash(data, i, j, flashed, count):
    flashed.append((i,j))
    count[0] += 1
    for a in get_adjacent(i, j):
        k, l = a
        increase_single(data, k, l)
        check_flash_single(data, k, l, flashed, count)

flashed = []
res = [0]

# part 1

for _ in range(DAYS):
    reset(data, flashed)
    flashed = []
    increase(data)
    check_flash(data, flashed, res)

print(res[0])

def has_sync(data):
    for row in data:
        for v in row:
            if v != 0:
                return False
    return True

# part 2

days = DAYS
while True:
    reset(data, flashed)
    flashed = []
    if has_sync(data):
        break
    increase(data)
    check_flash(data, flashed, res)
    days += 1

print(days)
