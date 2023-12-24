from math import copysign

# parse moves
with open("input", "r") as file:
    input: list[tuple[str, str]] = [
        tuple(line.replace("\n", "").split(" ")) for line in file.readlines()
    ]
moves: list[tuple[str, int]] = [(line[0], int(line[1])) for line in input]


def adjust_tail(head, tail):
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    has_moved = False
    if abs(dx) > 1 or (abs(dx) > 0 and abs(dy) > 1):
        n = int(copysign(1, dx))
        tail = (tail[0] + n, tail[1])
        has_moved = True
    if abs(dy) > 1 or (abs(dy) > 0 and abs(dx) > 1):
        n = int(copysign(1, dy))
        tail = (tail[0], tail[1] + n)
        has_moved = True
    return tail, has_moved


def process(n):
    visited: list[tuple[int, int]] = [(0, 0)]
    nodes: list[tuple[int, int]] = [(0, 0) for n in range(n)]

    for m in moves:
        for n in range(m[1]):
            # move the head first
            h, t = (nodes[0], nodes[1])
            res = {
                "L": (h[0] - 1, h[1]),
                "R": (h[0] + 1, h[1]),
                "U": (h[0], h[1] + 1),
                "D": (h[0], h[1] - 1),
            }
            h = res[m[0]]
            nodes[0] = h

            # adjust all the other bits
            has_moved = False
            for i in range(len(nodes) - 1):
                h, t = (nodes[i], nodes[i + 1])
                t, has_moved = adjust_tail(h, t)
                nodes[i + 1] = t
            if has_moved:
                visited.append(t)
    return len(set(visited))

print(process(2))  # part one
print(process(10)) # part two
