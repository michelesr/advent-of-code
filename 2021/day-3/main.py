from collections import Counter

with open("input", "r") as f:
    numbers = [l.strip() for l in f.readlines()]

# part 1

res = []

for i in range(0, len(numbers[0])):
    bits = [x[i] for x in numbers]
    zeros = [x for x in bits if x == '0']
    ones = [x for x in bits if x == '1']
    if len(zeros) > len(ones):
        res.append(0)
    else:
        res.append(1)

inv = [(x + 1) % 2 for x in res]
res = ''.join([str(x) for x in res])
inv = ''.join([str(x) for x in inv])

a, b = int(res, 2), int(inv, 2)
print(a * b)

# part 2

def get_bits(numbers, i):
    return [number[i] for number in numbers]

def get_keep(c, least=False):
    if least:
        keep = '0'
        if c['1'] < c['0']:
            keep = '1'
    else:
        keep = '1'
        if c['0'] > c['1']:
            keep = '0'
    return keep

def check_numbers(numbers, i, least=False):
    bits = get_bits(numbers, i)
    c = Counter(bits)
    keep = get_keep(c, least)
    return list(filter(lambda e: e[i] == keep, numbers))

def run_check(numbers, least=False):
    res, i = numbers, 0
    while len(res) > 1:
        res = check_numbers(res, i, least)
        i += 1
    return res[0]

a, b = run_check(numbers, False), run_check(numbers, True)
a, b = int(a, 2), int(b, 2)
print(a * b)
