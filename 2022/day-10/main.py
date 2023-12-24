x = 1
cycles = 0
signal_str = []
crt_out = ["." for i in range(40 * 6)]


def crt_draw(pos, x):
    if pos % 40 in (x, x - 1, x + 1):
        crt_out[pos] = "#"


with open("input", "r") as file:
    input = [line.strip("\n") for line in file.readlines()]

# execute the instructions
for instruction in input:
    cycles += 1
    crt_draw(cycles - 1, x)
    if (cycles + 20) % 40 == 0 and cycles <= 220:
        signal_str.append(cycles * x)
    parts = instruction.split(" ")
    instruction = parts[0]
    value = parts[1] if len(parts) > 1 else 0
    if instruction == "addx":
        cycles += 1
        crt_draw(cycles - 1, x)
        if (cycles + 20) % 40 == 0 and cycles <= 220:
            signal_str.append(cycles * x)
        x += int(value)

# part one: sum of signal strenghts
print(sum(signal_str))

# part two: draw the crt output
for i in range(6):
    for j in range(40):
        print(crt_out[40 * i + j], end="")
    print()
