from copy import deepcopy


class Monkey:
    inspected = 0

    def __init__(
        self,
        items: list[int],
        op: tuple[str, str],
        test_div: int,
        true_m: int,
        false_m: int,
        relief: bool = True,
    ):
        self.items = items
        self.op = op
        self.test_div = test_div
        self.true_m = true_m
        self.false_m = false_m
        self.relief = relief

    def inspect_all(self, monkeys: list["Monkey"]):
        items = self.items.copy()
        for i in range(len(items)):
            item, test = self.inspect(self.items[i])
            if test:
                monkeys[self.true_m].items.append(item)
            else:
                monkeys[self.false_m].items.append(item)
        self.items = []

    def inspect(self, item: int) -> tuple[int, bool]:
        self.inspected += 1
        item = self.apply_op(item)
        if self.relief:
            item //= 3
        else:
            item = item % p
        return item, item % self.test_div == 0

    def apply_op(self, item: int) -> int:
        operator, operand = self.op
        if operand == "old":
            operand = item
        else:
            operand = int(operand)
        res = -1
        match operator:
            case "+":
                res = item + operand
            case "*":
                res = item * operand
        return res

    def __repr__(self):
        return f"Monkey(items: {self.items}, op: {self.op}, test_div: {self.test_div}, true_m: {self.true_m}, false_m: {self.false_m}, inspected: {self.inspected})"


def result(monkeys: list[Monkey]) -> int:
    values = list(map(lambda x: x.inspected, monkeys))
    values = list(sorted(values))[-2:]
    return values[0] * values[1]


with open("input", "r") as file:
    input = [line.strip("\n") for line in file.readlines()]

monkeys: list[Monkey] = []
i = 0
divisors = set()

while True:
    if input[i] == "":
        i += 1
    i += 1
    items = input[i].split(":")[1].split(",")
    items = [int(item) for item in items]
    i += 1
    op = tuple(input[i].split("=")[1].split(" ")[-2:])
    i += 1
    test_div = int(input[i].split("by")[1])
    divisors.add(test_div)
    i += 1
    true_m = int(input[i].split("monkey")[1])
    i += 1
    false_m = int(input[i].split("monkey")[1])
    i += 1
    monkeys.append(Monkey(items, op, test_div, true_m, false_m))
    if i >= len(input):
        break

p = 1
for divisor in divisors:
    p *= divisor

# part one
old_monkeys = deepcopy(monkeys)
for i in range(20):
    for monkey in monkeys:
        monkey.inspect_all(monkeys)
print(result(monkeys))

# part two
monkeys = old_monkeys
for monkey in monkeys:
    monkey.relief = False
for i in range(10000):
    for monkey in monkeys:
        monkey.inspect_all(monkeys)
print(result(monkeys))
