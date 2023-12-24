with open('input', 'r') as f:
    data = [list(x) for x in [l.strip() for l in f.readlines()]]

MAX_I, MAX_J = len(data) - 1, len(data[0]) - 1

def get_adjacent(i, j):
    res = []
    if i > 0:
        res.append((i - 1, j))
    if i < MAX_I:
        res.append((i + 1, j))
    if j > 0:
        res.append((i, j - 1))
    if j < MAX_J:
        res.append((i, j + 1))
    return res

# part 1

res, lp = 0, []
for i in range(len(data)):
    for j in range(len(data[i])):
        adj = tuple(map(lambda k: data[k[0]][k[1]], get_adjacent(i, j)))

        if data[i][j] < min(adj):
            res += int(data[i][j]) + 1
            # store the coords of the point for part 2
            lp.append((i, j))

print(res)

# part 2

def update_res(size, res):
    res.append(size[0])
    if len(res) > 3:
        res.remove(min(res))

def check_point(i, j, checked, size):
    checked.append((i, j))

    if int(data[i][j]) != 9:
        size[0] += 1

        for p in get_adjacent(i, j):
            k, l = p[0], p[1]
            if not (k, l) in checked:
                check_point(k, l, checked, size)

res, checked = [], []
for p in lp:
    size, i, j = [0], p[0], p[1]
    check_point(i, j, checked, size)
    update_res(size, res)

print(res[0] * res[1] * res[2])
