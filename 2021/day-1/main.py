with open("input", "r") as f:
    numbers = [int(l) for l in f.readlines()]

# part 1
count, last = 0, -1
for n in numbers:
    if last > 0 and n > last:
        count += 1
    last = n
print(count)

# part 2
count, last = 0, -1
for i in range(3, len(numbers)):
    s = sum(numbers[i-3:i])
    if sum(numbers[i-3:i]) > last:
        count +=1
    last = s

print(count)
