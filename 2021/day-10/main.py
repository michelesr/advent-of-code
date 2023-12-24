from statistics import median

MAP = {'(': ')', '[': ']', '{': '}', '<': '>'}

with open('input', 'r') as f:
    lines = [l.strip() for l in f.readlines()]

# part 1

def check_line(line):
    stack = []
    for char in line:
        if char in MAP.values():
            if len(stack) == 0:
                return char
            c = stack.pop()
            if MAP[c] != char:
                return char
        else:
            stack.append(char)
    # stack is used for part 2
    return stack

res, scores = 0, {')': 3, ']': 57, '}' : 1197, '>': 25137}
for line in lines:
    c = check_line(line)
    if type(c) == str:
        res += scores[c]

print(res)

# part 2

# keep incomplete lines only
lines = filter(lambda l: type(check_line(l)) == list, lines)

def complete(line):
    stack = check_line(line)
    if type(stack) != list:
        raise TypeError("corrupted line: '{}' '{}'".format(line, stack))
    return list(map(lambda c: MAP[c], reversed(stack)))

def score(line):
    res, scores = 0, {')': 1, ']': 2, '}' : 3, '>': 4}
    for char in line:
        res *= 5
        res += scores[char]
    return res

res = map(complete, lines)
print(median(list(map(score, res))))
