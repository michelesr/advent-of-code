import re

R = re.compile(r"(?<![\?#])#+(?![\?#])")

def final_check_input(input, nums):
    matches = re.findall(r"#+", input)
    lens = [len(x) for x in matches]
    return lens == nums


def check_input(input, nums):
    matches = R.findall(input)
    lens = [len(x) for x in matches]
    nc = nums.copy()
    for x in lens:
        if x in nc:
            nc.remove(x)
        else:
            return False
    return True


def decode_input(input, nums, depth=1, max_depth=None, res=None):
    if max_depth is None:
        max_depth = len(re.findall(r"\?", input))
    if res is None:
        res = []
    inputs = [input.replace("?", "#", 1), input.replace("?", ".", 1)]
    for i in inputs:
        if check_input(i, nums):
            if depth < max_depth:
                decode_input(i, nums, depth=depth + 1, max_depth=max_depth, res=res)
            elif final_check_input(i, nums):
                res.append(i)
    return res


with open("./input") as f:
    lines = [line.strip().split(" ") for line in f.readlines()]
    lines = [[y[0], [int(x) for x in y[1].split(",")]] for y in lines]

# print(decode_input(*lines[47]))
print(sum([len(decode_input(*line)) for line in lines]))


for line in lines:
    line[0] += 4 * ("?" + line[0])
    line[1] *= 5

# for line in lines:
#     print(len(decode_input(*line)))

# too slow for part 2
# print(sum([len(decode_input(*line)) for line in lines]))
#
# print(lines[0])
