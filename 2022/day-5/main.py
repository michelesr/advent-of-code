from copy import deepcopy

with open("input", "r") as file:
    lines = [line.replace("\n", "") for line in file.readlines()]

stack_lines = lines[: lines.index("")]
num_of_stacks = int(stack_lines.pop().split(" ")[-2])

stacks = [list() for i in range(num_of_stacks)]
for line in reversed(stack_lines):
    for i in range(num_of_stacks):
        letter = line[i * 4 + 1]
        if letter != " ":
            stacks[i].append(letter)

instructions = lines[lines.index("") + 1 :]
instructions = [
    (int(part[1]), int(part[3]), int(part[5]))
    for part in [instruction.split(" ") for instruction in instructions]
]

original_stacks = deepcopy(stacks)
for instruction in instructions:
    count, src, dest = instruction
    for i in range(count):
        stacks[dest - 1].append(stacks[src - 1].pop())

# part one
res = "".join([stack[-1] for stack in stacks])
print(res)

stacks = original_stacks

for instruction in instructions:
    count, src, dest = instruction
    tmp = []
    for i in range(count):
        tmp.append(stacks[src - 1].pop())
    stacks[dest - 1] += list(reversed(tmp))

# part two
res = "".join([stack[-1] for stack in stacks])
print(res)
