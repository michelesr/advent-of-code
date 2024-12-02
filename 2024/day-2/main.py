from os import getenv

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    reports = [[int(num) for num in line.split(" ")] for line in f.readlines()]


def get_sign(n: int) -> int:
    return 0 if n == 0 else 1 if n > 0 else -1


def check_report(report: list[int], correct: bool = False) -> bool:
    sign = None

    for i in range(len(report) - 1):
        d = report[i] - report[i + 1]
        new_sign = get_sign(d)
        if sign is None:
            sign = new_sign
        if new_sign != sign or d == 0 or abs(d) > 3:
            if correct:
                for n in (0, 1, -1):
                    new_report = report.copy()
                    del new_report[i + n]
                    if check_report(new_report):
                        return True
            return False
    return True


print(len([r for r in reports if check_report(r)]))
print(len([r for r in reports if check_report(r, True)]))
