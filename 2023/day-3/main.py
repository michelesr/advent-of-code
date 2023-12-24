with open("./input") as f:
    lines = [line.strip() for line in f.readlines()]


def find_adj_symbol(i, j):
    """Return the position of the adj symbol or False if not found"""
    for pos in [
        (i - 1, j - 1),
        (i - 1, j + 1),
        (i - 1, j),
        (i + 1, j),
        (i + 1, j + 1),
        (i + 1, j - 1),
        (i, j + 1),
        (i, j - 1),
    ]:
        try:
            e = lines[pos[0]][pos[1]]
            if e != "." and not e.isdigit():
                return pos
        except IndexError:
            pass
    return False


def check_adj(i, start, end):
    j = start
    while j < end:
        pa = find_adj_symbol(i, j)
        if pa:
            return pa
        j += 1
    return False


def find_part_number(i, j) -> tuple[int, int]:
    start = j
    while lines[i][start].isdigit() and start >= 0:
        start -= 1
    start += 1
    end = j
    try:
        while lines[i][end].isdigit() and end <= len(lines):
            end += 1
    except IndexError:
        pass
    return (start, end)


def check_sym(i, j):
    """Check if the symbol has another adj part number"""
    # row number and start-end slice
    matches: set[tuple[int, tuple[int, int]]] = set()
    for pos in [
        (i - 1, j - 1),
        (i - 1, j + 1),
        (i - 1, j),
        (i + 1, j),
        (i + 1, j + 1),
        (i + 1, j - 1),
        (i, j + 1),
        (i, j - 1),
    ]:
        try:
            e = lines[pos[0]][pos[1]]
            if e.isdigit():
                p = find_part_number(pos[0], pos[1])
                if p:
                    matches.add((pos[0], p))
                assert not len(p) > 2
                if len(matches) == 2:
                    m = list(matches)
                    mi = m[0][0]
                    ms, me = m[0][1]
                    a = int("".join(lines[mi][ms:me]))
                    mi = m[1][0]
                    ms, me = m[1][1]
                    b = int("".join(lines[mi][ms:me]))
                    return a * b
        except IndexError:
            continue
    return False


res = 0
symbols = set()
for i in range(len(lines)):
    j = 0
    while j < len(lines[0]):
        if lines[i][j].isdigit():
            start = end = j
            while lines[i][end].isdigit():
                end += 1
                if end >= len(lines[0]):
                    break
            # NOTE: end is after the last digit
            pos = check_adj(i, start, end)
            if pos:
                n = int("".join(lines[i][start:end]))
                res += n
                # move the cursor to the end of the number
                j = end
                x, y = pos
                if lines[x][y] == "*":
                    symbols.add(pos)
                continue
        j += 1

print(res)
powers = [check_sym(sym[0], sym[1]) for sym in symbols]
print(sum(powers))
