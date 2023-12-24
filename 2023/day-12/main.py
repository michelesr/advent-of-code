from sys import argv


# i -> input cursor
# j -> nums cursor
# k -> used to track the length of the # blocks
def count_alternatives(input, nums, i=0, j=0, k=0, reset=True, results={}):
    if reset:
        results.clear()
    key = (i, j, k)
    if key in results:
        return results[key]
    res = 0

    # reached the end of the input
    if i == len(input):
        # checked all the blocks and cursor is not on a block
        if j == len(nums) and k == 0:
            return 1
        # cursor is on a block so check last block
        elif j == (len(nums) - 1) and nums[j] == k:
            return 1
        # not enough blocks found
        else:
            return 0
    for c in [".", "#"]:
        if input[i] == c or input[i] == "?":
            # outside a block and moving to the next input element
            if c == "." and k == 0:
                res += count_alternatives(input, nums, i + 1, j, 0, False)
            # check the block before exiting, updating j to point to the new block with initial size k=0
            elif c == "." and k > 0 and j < len(nums) and nums[j] == k:
                res += count_alternatives(input, nums, i + 1, j + 1, 0, False)
            # increase the current block size by 1, so that it can be checked later
            elif c == "#":
                res += count_alternatives(input, nums, i + 1, j, k + 1, False)
    results[key] = res
    return res


def run(lines):
    print(sum([count_alternatives(*line, reset=True) for line in lines]))


filename = "./input"
if len(argv) >= 2:
    filename = argv[1]

with open(filename) as f:
    lines = [line.strip().split(" ") for line in f.readlines()]
    lines = [[y[0], [int(x) for x in y[1].split(",")]] for y in lines]

run(lines)
for line in lines:
    line[0] += 4 * ("?" + line[0])
    line[1] *= 5
run(lines)
