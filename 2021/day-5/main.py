count = 0
grid = [[0 for i in range(1000)] for j in range(1000)]

with open("input", "r") as f:
    lines = []
    for l in f.readlines():
        parts = l.strip().split(' ')
        a, b = parts[0].split(',')
        c, d = parts[2].split(',')

        lines.append([[int(a), int(b)], [int(c), int(d)]])

for l in lines:
    x, y = 0, 1
    a, b = l[0], l[1]

    # straight
    if a[x] == b[x] or a[y] == b[y]:
        for i in range(min(a[x], b[x]), max(a[x], b[x]) + 1):
            for j in range(min(a[y], b[y]), max(a[y], b[y]) + 1):
                grid[i][j] += 1
                if grid[i][j] == 2:
                    count += 1

    # diagonal
    else:
        if a[x] > b[x]:
            a, b = b, a
        assert a[x] < b[x]

        if a[y] < b[y]:
            s = 1
        else:
            s = -1

        j = a[y]
        for i in range(min(a[x], b[x]), max(a[x], b[x]) + 1):
            grid[i][j] += 1
            if grid[i][j] == 2:
                count += 1
            j += s

print(count)
