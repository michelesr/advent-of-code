def cd(dir: str):
    global pwd, wd
    if dir == "/":
        pwd = ["/"]
        wd = fs["/"]
    elif dir == "..":
        pwd.pop()
        wd = fs["/"]
        for key in pwd[1:]:
            wd = wd[key]
    else:
        pwd.append(dir)
        wd = wd[dir]


def visit(wd=None):
    size = 0
    global fs, sums
    if not wd:
        wd = fs["/"]
    for k, v in wd.items():
        if isinstance(v, dict):
            size += visit(v)
        else:
            size += v
    sums.append(size)
    return size


fs = {"/": {}}
pwd = ["/"]
wd = fs["/"]
sums = []

with open("input", "r") as file:
    input: list[str] = [line.replace("\n", "") for line in file.readlines()]

for line in input:
    parts = line.split(" ")
    if parts[0] == "$":
        if parts[1] == "cd":
            cd(parts[2])
        elif parts[1] == "ls":
            pass
    elif parts[0] == "dir":
        wd[line.split(" ")[1]] = {}
    elif parts[0].isnumeric():
        size = int(parts[0])
        name = parts[1]
        wd[name] = size
    else:
        raise ValueError(f"unknown token on line {line}")

visit()

# part one
res = sum([s for s in sums if s <= 100000])
print(res)

# part two
sums = list(sorted(sums))
REQUIRED_SPACE = 30000000
TOTAL_SPACE = 70000000
used_space = sums[-1]
available_space = TOTAL_SPACE - used_space
space_to_free = 30000000 - available_space
for sum in sums:
    if sum >= space_to_free:
        print(sum)
        break
