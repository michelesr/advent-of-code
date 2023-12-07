def range_overlap(x, y):
    return range(max(x[0], y[0]), min(x[-1], y[-1]) + 1)


def process_data(data):
    for rules in maps:
        for i in range(len(data)):
            for rule in rules:
                dest, src, length = rule
                src_range = range(src, src + length)
                dest_range = range(dest, dest + length)
                if data[i] in src_range:
                    data[i] = dest_range[src_range.index(data[i])]
                    break


def process_data2(data):
    for rules in maps:
        processed = []
        for rule in rules:
            dest, src, length = rule
            src_range = range(src, src + length)
            dest_range = range(dest, dest + length)
            for element in data.copy():
                if element in processed:
                    continue
                overlap = range_overlap(src_range, element)
                if len(overlap) > 0:
                    # remove original element from data
                    data.remove(element)
                    # add the overlap as processed data to avoid reprocessing
                    # during the same ruleset
                    a = src_range.index(overlap[0])
                    b = src_range.index(overlap[-1])
                    new = range(dest_range[a], dest_range[b] + 1)
                    data.append(new)
                    processed.append(new)
                    # add the unprocessed data
                    for r in (
                        range(element[0], overlap[0]),
                        range(overlap[-1] + 1, element[-1] + 1),
                    ):
                        if len(r) > 0:
                            data.append(r)


with open("./input") as f:
    lines = f.readlines()

# get the seeds
seeds = [int(n) for n in lines[0].strip().split(": ")[1].split(" ")]

i = 0
maps = []
current = []
for line in lines[3:]:
    if line == "\n":
        i += 1
        maps.append(current)
        current = []
    elif line[0].isdigit():
        current.append([int(num) for num in line.strip().split(" ")])
maps.append(current)

# part 1
data = seeds.copy()
process_data(data)
print(min(data))

# part 2
data = []
for i in range(len(seeds)):
    if i % 2 == 0:
        data.append(range(seeds[i], seeds[i] + seeds[i + 1]))
process_data2(data)
print(min([r[0] for r in data]))
