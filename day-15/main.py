from sys import argv

boxes = {}


def op_insert(label: str, power: int):
    box_id = calculate_hash(label)
    if box_id not in boxes:
        boxes[box_id] = {}
    boxes[box_id][label] = power


def op_remove(label: str):
    box_id = calculate_hash(label)
    if box_id not in boxes:
        return
    if label in boxes[box_id]:
        del boxes[box_id][label]


def score() -> int:
    res = 0
    for box_id, lenses in boxes.items():
        for i, lens in enumerate(lenses.keys()):
            res += (box_id + 1) * (i + 1) * lenses[lens]
    return res


def calculate_hash(s: str) -> int:
    current = 0
    for char in s:
        current += ord(char)
        current *= 17
        current %= 256
    return current


filename = "./input"
if len(argv) >= 2:
    filename = argv[1]

with open(filename) as f:
    data = f.readline().strip().split(",")

print(sum([calculate_hash(s) for s in data]))

for instruction in data:
    if "=" in instruction:
        label, power = instruction.split("=")
        op_insert(label, int(power))
    elif "-" in instruction:
        label = instruction.split("-")[0]
        op_remove(label)
    else:
        raise ValueError("Invalid instruction")

print(score())
