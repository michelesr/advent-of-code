from os import getenv

def count_combinations(s, substrings):
    def count_combinations_recursive(s, substrings, memo):
        if s in memo:
            return memo[s]
        if not s:
            return 1
        count = 0
        for substring in substrings:
            if s.startswith(substring):
                count += count_combinations_recursive(s[len(substring):], substrings, memo)
        memo[s] = count
        return count

    memo = {}
    return count_combinations_recursive(s, substrings, memo)

with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    lines = [line.strip() for line in f.readlines()]

towels = set(lines[0].split(', '))
designs = lines[2:]


res = [count_combinations(design, towels) for design in designs]
print(sum(bool(x) for x in res))
print(sum(res))
