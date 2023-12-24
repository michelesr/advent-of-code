with open('input', 'r') as f:
    lines = [l.strip() for l in f.readlines() if l.strip() != '']

folds = filter(lambda l: '=' in l, lines)
folds = map(lambda l: l.split(' ')[2].split('='), folds)
folds = map(lambda p: (p[0], int(p[1])), folds)

coords = map(lambda l: l.split(','), filter(lambda l: ',' in l, lines))
coords = list(map(lambda p: (int(p[0]), int(p[1])), coords))

def get_paper_size(coords):
    x = max(map(lambda p: p[0], coords)) + 1
    y = max(map(lambda p: p[1], coords)) + 1
    return x, y

def plot(coords):
    X, Y = get_paper_size(coords)
    for y in range(Y):
        for x in range(X):
            if (x, y) in coords:
                print('#', end='')
            else:
                print('.', end='')
        print()

def fold_paper(fold, coords):
    X, Y = get_paper_size(coords)
    if fold[0] == 'x':
        coords = fold_paper_x(fold[1], coords)
    else:
        coords = fold_paper_y(fold[1], coords)
    return coords

def fold_coord_x(coord, fold):
    x, y = coord
    if x > fold:
        return (2 * fold - x, y)
    else:
        return coord

def fold_coord_y(coord, fold):
    x, y = coord
    if y > fold:
        return (x, 2 * fold - y)
    else:
        return coord

def fold_paper_x(fold, coords):
    return list(set(map(lambda c: fold_coord_x(c, fold), coords)))

def fold_paper_y(fold, coords):
    return list(set(map(lambda c: fold_coord_y(c, fold), coords)))

dots = []
for fold in folds:
    coords = fold_paper(fold, coords)
    dots.append(len(coords))

# part 1
print(dots[0])

# part 2
plot(coords)
