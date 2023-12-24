from collections import Counter

with open('input', 'r') as f:
    template = f.readline().strip()
    f.readline()
    rules = [l.strip() for l in f.readlines()]

rules = map(lambda l: tuple(l.split(' -> ')), rules)

rules_map = {}
for rule in rules:
    rules_map[(rule[0][0], rule[0][1])] = ((rule[0][0], rule[1]), (rule[1], rule[0][1]))

def get_pairs(template):
    res = [(None, template[0])]
    for i in range(len(template) - 1):
        res.append((template[i], template[i+1]))
    res.append((template[-1], None))
    return res

# transform into pair counter
template = Counter(get_pairs(template))

def expand(counter):
    res = counter.copy()
    for k, v in counter.items():
        if k in rules_map.keys():
            res[k] -= v
            for p in rules_map[k]:
                res[(p[0], p[1])] = res.get((p[0], p[1]), 0) + v
    return res

def count(counter):
    res = {}
    for k, v in counter.items():
        for n in k:
            if n != None and v > 0:
                res[n] = res.get(n, 0) + v
    return {k: v // 2  for k, v in res.items()}

def res(template, n):
    for _ in range(n):
        template = expand(template)

    c = count(template).values()
    return (max(c) - min(c))

print(res(template, 10))
print(res(template, 40))
