from os import getenv

def solve(machine):
    a_x, a_y = machine["a_x"], machine["a_y"]
    b_x, b_y = machine["b_x"], machine["b_y"]
    prize_x, prize_y = machine["prize_x"], machine["prize_y"]

    # create the matrix for the linear system
    a1, b1, c1 = a_x, b_x, prize_x
    a2, b2, c2 = a_y, b_y, prize_y

    # solve with cramer
    return (
        (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1),
        (c2 * a1 - c1 * a2) / (a1 * b2 - a2 * b1)
    )

def is_valid_solution(a, b):
    return int(a) == a and int(b) == b

def total_cost(machines) -> int:
    res = 0
    for machine in machines:
        a, b = solve(machine)
        if is_valid_solution(a, b):
            res += 3 * a + b
    if int(res) != res:
        raise ValueError("Non integer solution")
    return int(res)


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    lines = f.readlines()

machines = []
machine = {}

for line in lines:
    line = line.strip()
    if line.startswith("Button A:"):
        # Parse the X and Y movements for button A
        parts = line.split(": ")[1].split(", ")
        machine["a_x"] = int(parts[0].split("+")[1])
        machine["a_y"] = int(parts[1].split("+")[1])
    elif line.startswith("Button B:"):
        # Parse the X and Y movements for button B
        parts = line.split(": ")[1].split(", ")
        machine["b_x"] = int(parts[0].split("+")[1])
        machine["b_y"] = int(parts[1].split("+")[1])
    elif line.startswith("Prize:"):
        # Parse the prize location
        parts = line.split(": ")[1].split(", ")
        machine["prize_x"] = int(parts[0].split("=")[1])
        machine["prize_y"] = int(parts[1].split("=")[1])
        machines.append(machine)
        machine = {}

print(total_cost(machines))

for machine in machines:
    machine["prize_x"] += 10000000000000
    machine["prize_y"] += 10000000000000

print(total_cost(machines))
