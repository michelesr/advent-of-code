from os import getenv

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    rotations = [(line[0], int(line[1:])) for line in f.readlines()]

position = 50

# times the rotation passes through 0 without stopping
count = 0
# times the rotation ends on 0
zeros = 0

for dir, steps in rotations:
    start = position
    match dir:
        case 'L':
            position -= steps
        case 'R':
            position += steps
    cycles = abs(position // 100)
    if start == 0 and position < 0:
        # we already counted this zero in zeros
        cycles -= 1
    position %= 100
    if position == 0:
        zeros += 1
        # because we counted the zero in zeros, remove 1 cycle to balance
        if dir == 'R' and cycles > 0:
            cycles -= 1
    count += cycles
    # print(dir, steps, position, cycles)

print(zeros)
print(count + zeros)
