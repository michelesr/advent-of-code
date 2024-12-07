from os import getenv
import itertools


def compute(equations, operators):
    anwser = 0
    for eq in equations:
        operands = eq[1]
        n_op = len(eq[1]) - 1
        found = False
        combinations = itertools.product(operators, repeat=n_op)
        while not found and (combination := next(combinations, None)):
            res = operands[0]
            for i in range(len(combination)):
                match combination[i]:
                    case "+":
                        res += operands[i + 1]
                    case "*":
                        res *= operands[i + 1]
                    case "||":
                        res = int(f"{res}{operands[i + 1]}")
            if res == eq[0]:
                anwser += res
                found = True
    return anwser


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    equations = [
        (int(e[0][:-1]), [int(x) for x in e[1:]])
        for e in [l.split(" ") for l in [line.strip() for line in f.readlines()]]
    ]

print(compute(equations, ["+", "*"]))
print(compute(equations, ["+", "*", "||"]))
