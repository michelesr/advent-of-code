from os import getenv

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    banks = [line.strip() for line in f.readlines()]


def get_output(banks: list[str], k: int) -> int:
    res = 0
    for bank in banks:
        n = int("".join(get_numbers(bank, k - 1)))
        # print(n)
        res += n
    return res


def get_numbers(bank: str, remaining: int) -> str:
    if remaining == 0:
        return max(bank)
    window = bank[:-remaining]
    m = max(window)
    i = bank.index(m)
    return max(window) + get_numbers(bank[i + 1 :], remaining - 1)


print(get_output(banks, 2))
print(get_output(banks, 12))
