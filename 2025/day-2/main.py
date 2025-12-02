from os import getenv
import re

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    ranges = f.readline().strip().split(',')
    ranges = [range(int(a), int(b) + 1) for a, b in [r.split('-') for r in ranges]]

# patterns
one, two = re.compile(r'^(.*)\1$'), re.compile(r'^(.*)\1+$')

res_one = 0
res_two = 0

for r in ranges:
    for n in r:
        if re.match(one, str(n)):
            res_one += n
            res_two += n
        elif re.match(two, str(n)):
            res_two += n
            
print(res_one)
print(res_two)
