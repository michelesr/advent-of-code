from collections import Counter

# change to 80 for part 1
DAYS = 256
with open("input", "r") as f:
    fishes = Counter([int(x) for x in f.readline().strip().split(',')])

for day in range(DAYS):
    old = dict(fishes)

    for x in range(9):
        if x not in old:
            old[x] = 0

    new = Counter({0: old[1], 1: old[2], 2: old[3], 3: old[4], 4: old[5], 5: old[6], 6: old[7], 7: old[8], 8: old[0]})
    fishes = new + Counter({6: old[0]})

res = 0
fishes = dict(fishes)
for k,v in fishes.items():
    res += v
print(res)
