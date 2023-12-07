NUMS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

with open("input", "r") as f:
    lines = list(f.readlines())


def make_num(line):
    line = [c for c in list(line) if c.isdigit()]
    return int("".join([line[0], line[-1]]))


sum = 0
for line in lines:
    if line != "\n":
        line = [c for c in list(line) if c.isdigit()]
        sum += make_num(line)
print(sum)


def find_last(line):
    NUMS = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    i = len(line)
    while i > 0:
        i -= 1
        for n in range(10):
            if str(n) in line[i:]:
                return n
        for k, v in NUMS.items():
            if k in line[i:]:
                return v


def find_first(line):
    i = 0
    while i < len(line):
        i += 1
        for n in range(10):
            if str(n) in line[:i]:
                return n
        for k, v in NUMS.items():
            if k in line[:i]:
                return v


sum = 0
for line in lines:
    if line != "\n":
        sum += 10 * find_first(line) + find_last(line)
print(sum)
