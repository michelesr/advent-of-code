with open("input", "r") as f:
    grid = [e for e in [list(line.replace("\n", "")) for line in f.readlines()]]

a = len(grid)  # len of a col
b = len(grid[0])  # len of a row
max_score = 0  # scenic score

# edge trees are always visible
res = (a * 2) + (b * 2) - 4

# not considering edge trees: scenic score is always 0
# as at least one of thier view distances is 0
for i in range(1, a - 1):
    for j in range(1, b - 1):
        tree = grid[i][j]

        # view distances
        ld = rd = ud = dd = 0

        # visible from at least one direction
        visible = False

        # check left
        ok = True
        for k in range(j - 1, -1, -1):
            ld += 1
            if tree <= grid[i][k]:
                ok = False
                break
        if ok:
            visible = True

        # check right
        ok = True
        for k in range(j + 1, b):
            rd += 1
            if tree <= grid[i][k]:
                ok = False
                break
        if ok:
            visible = True

        # check up
        ok = True
        for k in range(i - 1, -1, -1):
            ud += 1
            if tree <= grid[k][j]:
                ok = False
                break
        if ok:
            visible = True

        # check down
        ok = True
        for k in range(i + 1, a):
            dd += 1
            if tree <= grid[k][j]:
                ok = False
                break
        if ok:
            visible = True

        if visible:
            res += 1

        score = ld * rd * ud * dd
        max_score = max(max_score, score)

print(res)
print(max_score)
