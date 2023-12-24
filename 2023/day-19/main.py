from sys import argv
from operator import mul
from functools import reduce


def score_part(part: dict[str, int]) -> int:
    return sum(part.values())


def parse_rules(lines) -> dict[str, list[str]]:
    res = {}
    for line in lines:
        rule = line.split("{")
        key = rule[0]
        vals = rule[1][:-1].split(",")
        res[key] = vals
    return res


def parse_parts(lines: list[str]) -> list[dict[str, int]]:
    res = [line[1:-1].split(",") for line in lines]
    res = [[x.split("=") for x in y] for y in res]
    res = [{x[0]: int(x[1]) for x in y} for y in res]
    return res


def process_part(part: dict[str, int], rules: dict[str, list[str]]) -> bool:
    current = rules["in"]
    while True:
        for rule in current:
            if "<" in rule or ">" in rule:
                cond, body = rule.split(":")
                a, op, b = cond[0], cond[1], int(cond[2:])
                if op == "<":
                    cond = part[a] < b
                elif op == ">":
                    cond = part[a] > b
                else:
                    raise ValueError("Invalid operator")
                if cond:
                    if body == "A":
                        return True
                    elif body == "R":
                        return False
                    else:
                        current = rules[body]
                        break
            elif rule == "A":
                return True
            elif rule == "R":
                return False
            else:
                current = rules[rule]
                break


def length(comb: dict[str, range]) -> int:
    return reduce(mul, [len(r) for r in comb.values()], 1)


def process_range(comb: dict[str, range], rules: dict[str, list[str]]) -> int:
    res = 0
    current = rules["in"]
    done = False
    while not done:
        for rule in current:
            if rule == "A":
                done = True
                res += length(comb)
                break
            elif rule == "R":
                done = True
                break
            elif "<" in rule or ">" in rule:
                cond, body = rule.split(":")
                a, op, b = cond[0], cond[1], int(cond[2:])
                r = comb[a]
                if op == "<":
                    if not r[0] < b:
                        continue
                    # bad range, process again
                    y = comb.copy()
                    new = range(b, r[-1] + 1)
                    if len(new) > 0:
                        y[a] = new
                        res += process_range(y, rules)

                    # good range, continue with this
                    new = range(r[0], min(b, r[-1] + 1))
                    if len(new) <= 0:
                        done = True
                        break
                    comb[a] = new
                    if body == "A":
                        res += length(comb)
                        done = True
                        break
                    if body == "R":
                        done = True
                        break
                    else:
                        current = rules[body]
                        break
                elif op == ">":
                    if not r[-1] > b:
                        continue

                    # bad range, process again
                    y = comb.copy()
                    new = range(r[0], b + 1)
                    if len(new) > 0:
                        y[a] = range(r[0], max(r[0], b + 1))
                        res += process_range(y, rules)

                    # good range, continue with this
                    new = range(max(r[0], b + 1), r[-1] + 1)
                    if len(new) <= 0:
                        done = True
                        break
                    comb[a] = new

                    if body == "A":
                        res += length(comb)
                        done = True
                        break
                    if body == "R":
                        done = True
                        break
                    else:
                        current = rules[body]
                        break
            else:
                current = rules[rule]
                break
    return res


with open(argv[1]) as f:
    rules = []
    parts = []
    nl = False
    for line in f.readlines():
        if line == "\n":
            nl = True
            continue
        if nl:
            parts.append(line.strip())
        else:
            rules.append(line.strip())

parts = parse_parts(parts)
rules = parse_rules(rules)
print(sum([score_part(part) for part in parts if process_part(part, rules)]))

print(
    process_range(
        {
            "x": range(1, 4001),
            "m": range(1, 4001),
            "a": range(1, 4001),
            "s": range(1, 4001),
        },
        rules,
    )
)
