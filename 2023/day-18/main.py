from sys import argv


def perimeter(points: list[tuple[int, int]]) -> int:
    res = 0
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        ax, ay = a
        bx, by = b
        res += max(abs(ax - bx), abs(ay - by))
    return res


def area(points: list[tuple[int, int]]) -> int:
    # shoelace formula
    r1, r2 = 0, 0
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        ax, ay = a
        bx, by = b
        r1 += ax * by
        r2 += bx * ay
    return abs(r1 - r2) // 2


def find_points(
    lines: list[tuple[str, int, str]], part_two: bool = False
) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = [(0, 0)]
    x, y = 0, 0
    for line in lines:
        d, n = line[0], line[1]
        if part_two:
            h = line[2]
            d = int(h[-1])
            n = int(h[1:-1], 16)
        match d:
            case "L" | 2:
                x -= n
            case "R" | 0:
                x += n
            case "U" | 3:
                y += n
            case "D" | 1:
                y -= n
        points.append((x, y))
    return points


def score(points: list[tuple[int, int]]) -> int:
    # Pick's theorem
    #
    # A is the area of the polygon
    # b is the perimeter of the polygon
    # i is the number of integer points internal to the polygon
    #
    # i + b = A + b/2 + 1
    A = area(points)
    b = perimeter(points)
    res = A + b / 2 + 1
    return int(res)


lines = [line.strip().split(" ") for line in open(argv[1])]
lines = [(x[0], int(x[1]), x[2].replace("(", "").replace(")", "")) for x in lines]

print(score(find_points(lines)))
print(score(find_points(lines, part_two=True)))
