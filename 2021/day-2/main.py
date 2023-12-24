# horiz, depth, aim
pos = [0, 0, 0]

with open("input", "r") as f:
    moves = []
    for l in f.readlines():
        cmd, value = l.split(" ")
        moves.append([cmd, int(value)])

# part 1
for move in moves:
    if move[0] == 'forward':
        pos[0] += move[1]
    elif move[0] == 'down':
        pos[1] += move[1]
    elif move[0] == 'up':
        pos[1] -= move[1]

print(pos[0] * pos[1])

# part 2
for move in moves:
    if move[0] == 'forward':
        pos[0] += move[1]
        pos[1] += move[1] * pos[2]
    elif move[0] == 'down':
        pos[2] += move[1]
    elif move[0] == 'up':
        pos[2] -= move[1]

print(pos[0] * pos[1])
