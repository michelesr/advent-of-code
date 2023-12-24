from collections import Counter

def get_cost(positions, position):
    cost = 0
    for k,v in positions.items():
        steps = abs(k - position)
        cost += v * sum(range(1, steps + 1))
    return cost

with open("input", "r") as f:
    positions = Counter([int(x) for x in f.readline().strip().split(',')])

costs = {}
for position in positions:
    costs[position] = get_cost(positions, position)

print(min(costs.values()))
