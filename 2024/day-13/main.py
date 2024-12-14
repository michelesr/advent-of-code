from os import getenv


def calculate_cost(machine):
    """
    Calculate the cost of winning a prize for a given machine.

    Args:
    machine (dict): A dictionary containing the machine's configuration.

    Returns:
    int: The minimum cost to win the prize, or -1 if it's not possible.
    """
    a_x, a_y = machine["a_x"], machine["a_y"]
    b_x, b_y = machine["b_x"], machine["b_y"]
    prize_x, prize_y = machine["prize_x"], machine["prize_y"]

    min_cost = float("inf")

    # Iterate over all possible combinations of A and B presses
    for a_presses in range(101):
        for b_presses in range(101):
            # Calculate the total movement along the X and Y axes
            total_x = a_presses * a_x + b_presses * b_x
            total_y = a_presses * a_y + b_presses * b_y

            # Check if the prize can be reached
            if total_x == prize_x and total_y == prize_y:
                # Calculate the cost of winning the prize
                cost = a_presses * 3 + b_presses
                min_cost = min(min_cost, cost)

    return min_cost if min_cost != float("inf") else -1


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

res = 0
for machine in machines:
    cost = calculate_cost(machine)
    if cost != -1:
        res += cost

print(res)
