from dataclasses import dataclass
from itertools import combinations
from os import getenv

from numpy import array, ones
from scipy.optimize import linprog


@dataclass
class Machine:
    on: set[int]
    buttons: list[set[int]]
    joltage: list[int]

    def configure(self) -> int:
        # lazy and inefficient brute force
        for k in range(1, len(self.buttons)):
            for buttons in combinations(self.buttons, k):
                on = set()
                for button in buttons:
                    on = button ^ on
                if on == self.on:
                    return k
        raise ValueError("Invalid configuration")

    def configure_joltage(self) -> int:
        # the equations are describing the buttons that can be pressed to activate a specific joltage slot,
        # and the variables are the number of times they have to be activated,
        # with coefficient 1 if the button is linked to the desired joltage slot, or 0 if not
        # this is the lhs of the linear system
        equations = array(
            [
                [int(i in button) for button in self.buttons]
                for i in range(len(self.joltage))
            ]
        )
        # these are the desired number of button pressed for that joltage value, the rhs of the linear system
        joltage = array(self.joltage)

        # cost of each variable, since we want to minimize the sum, we use 1 for each variable
        # this is like -> c = array([1] * len(equations[0]))
        c = ones(len(equations[0]))

        # all variables must be integer (0 is continuos, 1 is integer)
        integrality = c

        # we wants our variables to be >= 0, so we give (0, +inf) as boundary
        bounds = (0, None)

        res = linprog(
            c=c, A_eq=equations, b_eq=joltage, integrality=integrality, bounds=bounds
        )

        return int(sum(res.x))


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    machines: list[Machine] = []
    for line in f.readlines():
        parts = line.split("]")
        on = {i for i, v in enumerate(parts[0][1:]) if v == "#"}
        buttons = [
            set(int(n) for n in button.replace(" ", "").replace("(", "").split(","))
            for button in parts[1].split(")")[:-1]
        ]
        joltage = [
            int(n)
            for n in parts[1]
            .split(") ")[-1]
            .replace("{", "")
            .replace("}", "")
            .split(",")
        ]
        machines.append(Machine(on=on, buttons=buttons, joltage=joltage))

print(sum(m.configure() for m in machines))
print(sum(m.configure_joltage() for m in machines))
