from os import getenv


def run_program(program, registers):
    instruction_pointer = 0
    output = []

    while 0 <= instruction_pointer < len(program):
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        denominator = None

        if opcode == 0:  # adv instruction
            # Perform division. The numerator is the value in the A register.
            # The denominator is found by raising 2 to the power of the instruction's combo operand.
            if operand < 4:
                denominator = 2**operand
            elif operand == 4:
                denominator = 2 ** registers["A"]
            elif operand == 5:
                denominator = 2 ** registers["B"]
            elif operand == 6:
                denominator = 2 ** registers["C"]

            if denominator is None:
                raise ValueError("No denominator")

            registers["A"] = registers["A"] // denominator

        elif opcode == 1:  # bxl instruction
            # Calculate the bitwise XOR of register B and the instruction's literal operand,
            # then stores the result in register B.
            registers["B"] = registers["B"] ^ operand

        elif opcode == 2:  # bst instruction
            # Calculate the value of its combo operand modulo 8,
            # then writes that value to the B register.
            if operand < 4:
                registers["B"] = operand % 8
            elif operand == 4:
                registers["B"] = registers["A"] % 8
            elif operand == 5:
                registers["B"] = registers["B"] % 8
            elif operand == 6:
                registers["B"] = registers["C"] % 8

        elif opcode == 3:  # jnz instruction
            # If the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand.
            if registers["A"] != 0:
                instruction_pointer = operand
                continue  # Do not increment instruction pointer

        elif opcode == 4:  # bxc instruction
            # Calculate the bitwise XOR of register B and register C, then stores the result in register B.
            registers["B"] = registers["B"] ^ registers["C"]

        elif opcode == 5:  # out instruction
            # Calculate the value of its combo operand modulo 8, then outputs that value.
            if operand < 4:
                output.append(str(operand))
            elif operand == 4:
                output.append(str(registers["A"] % 8))
            elif operand == 5:
                output.append(str(registers["B"] % 8))
            elif operand == 6:
                output.append(str(registers["C"] % 8))

        elif opcode == 6:  # bdv instruction
            # Perform division. The numerator is the value in the A register.
            # The denominator is found by raising 2 to the power of the instruction's combo operand.
            if operand < 4:
                denominator = 2**operand
            elif operand == 4:
                denominator = 2 ** registers["A"]
            elif operand == 5:
                denominator = 2 ** registers["B"]
            elif operand == 6:
                denominator = 2 ** registers["C"]

            registers["B"] = registers["A"] // denominator

        elif opcode == 7:  # cdv instruction
            # Perform division. The numerator is the value in the A register.
            # The denominator is found by raising 2 to the power of the instruction's combo operand.
            if operand < 4:
                denominator = 2**operand
            elif operand == 4:
                denominator = 2 ** registers["A"]
            elif operand == 5:
                denominator = 2 ** registers["B"]
            elif operand == 6:
                denominator = 2 ** registers["C"]

            registers["C"] = registers["A"] // denominator

        instruction_pointer += 2

    return ",".join(output)


# Read the input
with open(getenv("AOC_INPUT", "example_input.txt"), "r") as file:
    lines = file.readlines()

registers = {"A": 0, "B": 0, "C": 0}

program = None
for line in lines:
    line = line.strip()
    if line.startswith("Register A:"):
        registers["A"] = int(line.split(":")[-1])
    elif line.startswith("Register B:"):
        registers["B"] = int(line.split(":")[-1])
    elif line.startswith("Register C:"):
        registers["C"] = int(line.split(":")[-1])
    elif line.startswith("Program:"):
        program = [int(x) for x in line.split(":")[-1].split(",")]

if program is None:
    raise ValueError("No program")

# Run the program
output = run_program(program, registers)

print(output)

test_program = [0, 3, 5, 4, 3, 0]
test_registers = {"A": 0, "B": 0, "C": 0}

# Test that the computer is working fine with correct input
assert run_program(test_program, {"A": 117440, "B": 0, "C": 0}) == "0,3,5,4,3,0"

# Generate some in out to understand the pattern
# with open('out.csv', 'w') as f:
#     print(program)
#     f.write("input output\n")
#     for i in range(200000):
#         registers['A'] = i
#         f.write(f"{registers['A']} {run_program(program, registers)}\n")

# That tells us that the len of the output (in terms of numbers) is
# f(n) -> log8(n) + 1
# That inverted tells us to start looking for our solution at (8 ** l-1)
# but the range is too big for brute forcing all of team

l = len(program)
# n = 8 ** (l)

# n = 258394904395776

# this value was found brute forcing and trying to grep for patterns
# in a very long tedious process I have no idea how it works
n = 258394904396699

while True:
    out = run_program(program, {"A": n, "B": 0, "C": 0})
    l = len(out.split(","))
    if l < 16:
        break
    print(out, l, n)
    # this was kinda random too...
    n += (8**3) * 1
