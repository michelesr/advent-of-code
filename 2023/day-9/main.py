def reduce_history_line(line: list[int]) -> list[int]:
    res = []
    for i in range(len(line) - 1):
        res.append(line[i + 1] - line[i])
    return res


def get_full_history(line: list[int]) -> list[list[int]]:
    res = [line]
    current = line
    while not all([x == 0 for x in current]):
        current = reduce_history_line(current)
        res.append(current)
    return res


def get_history_value(line: list[int]) -> int:
    data = get_full_history(line)
    data[-1].append(0)
    for i in range(len(data) - 2, -1, -1):
        data[i].append(data[i][-1] + data[i + 1][-1])
    return data[0][-1]


def get_history_value_left(line: list[int]) -> int:
    data = get_full_history(line)
    data[-1].insert(0, 0)
    for i in range(len(data) - 2, -1, -1):
        data[i].insert(0, data[i][0] - data[i + 1][0])
    return data[0][0]


with open("./input") as f:
    lines = [[int(x) for x in line.strip().split(" ")] for line in f.readlines()]

print(sum([get_history_value(line) for line in lines]))
print(sum([get_history_value_left(line) for line in lines]))
