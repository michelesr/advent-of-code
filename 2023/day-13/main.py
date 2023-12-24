from sys import argv


def transpose(matrix):
    res = [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]
    return ["".join(row) for row in res]


def find_reflection(lines):
    for i in range(len(lines) - 1):
        if lines[i] == lines[i + 1]:
            res = i
            ok = True
            j = i - 1
            k = i + 2
            while j >= 0 and k < len(lines):
                if lines[j] != lines[k]:
                    ok = False
                    break
                j -= 1
                k += 1
            if ok:
                return res
    return -1


def almost_equal(a, b):
    res = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            res += 1
        if res > 1:
            return False
    return True


def compare_lines(a, b, can_fix):
    if a == b:
        return (True, can_fix)
    elif can_fix:
        can_fix = False
        return (almost_equal(a, b), can_fix)
    else:
        return (False, can_fix)


def find_reflection_2(lines):
    for i in range(len(lines) - 1):
        is_equal, can_fix = compare_lines(lines[i], lines[i + 1], True)
        if is_equal:
            res = i
            ok = True
            j = i - 1
            k = i + 2
            while j >= 0 and k < len(lines):
                is_equal, can_fix = compare_lines(lines[j], lines[k], can_fix)
                if not is_equal:
                    ok = False
                    break
                j -= 1
                k += 1
            if ok and not can_fix:
                return res
    return -1


filename = "./input"
if len(argv) >= 2:
    filename = argv[1]

with open(filename) as f:
    i = 0
    lines = []
    lines.append([])
    for line in f.readlines():
        if line == "\n":
            i += 1
            lines.append([])
        else:
            lines[i].append(line.strip())

for f in (find_reflection, find_reflection_2):
    res = 0
    for line in lines:
        i = f(line)
        if i != -1:
            res += (i + 1) * 100
        else:
            i = f(transpose(line))
            if i == -1:
                print(lines.index(line))
                raise ValueError("Couldn't find reflection")
            res += i + 1
    print(res)
