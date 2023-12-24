from itertools import chain
from collections import Counter

def parse(line):
    parts = line.split('|')
    return (parts[0].strip().split(' '), parts[1].strip().split(' '))

with open('input', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

lines = tuple(map(parse, lines))

# part 1

# just use the output values and count freq of 2, 4, 3, 7
values = map(lambda l: l[1], lines)
freqs = map(lambda l: [len(v) for v in l], values)
freqs = Counter(chain(*freqs))
res = freqs[2] + freqs[4] + freqs[3] + freqs[7]
print(res)

# part 2

# a possible wiring configuration
wires = [
    set(['a', 'b', 'c', 'e', 'f', 'g']),
    set(['c', 'f']),
    set(['a', 'c', 'd', 'e', 'g']),
    set(['a', 'c', 'd', 'f', 'g']),
    set(['b', 'c', 'd', 'f']),
    set(['a', 'b', 'd', 'f', 'g']),
    set(['a', 'b', 'd', 'e', 'f', 'g']),
    set(['a', 'c', 'f']),
    set(['a', 'b', 'c', 'd', 'e', 'f', 'g']),
    set(['a', 'b', 'c', 'd', 'f', 'g'])
]

# number of segments for each digit
lengths = tuple(map(lambda x: len(x), wires))

# generate a map of the lengths of intersection
# with known numbers and the corresponding number
len_map = {}
for i in (0, 2, 3, 5, 6, 9):
    res = (
        len(wires[i].intersection(wires[1])),
        len(wires[i].intersection(wires[4])),
        len(wires[i].intersection(wires[7])),
        len(wires[i].intersection(wires[8]))
    )
    len_map[res] = i

res = 0
for line in lines:
    # parse the input into sets
    w = tuple(map(lambda l: set(l), line[0]))

    # number -> representation; used in intersection below
    table = {}
    # representation -> number; used for decoding
    itable = {}

    # find 1, 4, 7, 8
    for i in (1, 4, 7, 8):
        # find the number using its segment count
        x = filter(lambda x: len(x) == lengths[i], w).__next__()

        # add it to the lookup tables
        table[i] = tuple(x)
        itable[tuple(x)] = i

    # leave only the unknown
    patterns = filter(lambda x: not tuple(x) in itable, w)

    # find the others
    for pattern in patterns:
        lens = (
            len(pattern.intersection(set(table[1]))),
            len(pattern.intersection(set(table[4]))),
            len(pattern.intersection(set(table[7]))),
            len(pattern.intersection(set(table[8])))
        )

        # find the number using the map created above
        n = len_map[lens]

        # add it to the lookup tables
        table[n] = tuple(pattern)
        itable[tuple(pattern)] = n

    # need to sort letters in the itable keys
    itable = {tuple(sorted(k)): v for k, v in itable.items()}

    # parse the output using the table
    out = tuple(map(lambda x: tuple(sorted(x)), line[1]))
    digits = map(lambda x: itable[tuple(x)], out)

    # build the number from the decimal digits
    n = (
        (10 ** 3) * digits.__next__() +
        (10 ** 2) * digits.__next__() +
        10 * digits.__next__() +
        digits.__next__()
    )

    # add it to the sum
    res += n

print(res)
