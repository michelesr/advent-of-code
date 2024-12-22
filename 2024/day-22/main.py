from os import getenv

def mix_and_prune(secret, value):
    mixed = secret ^ value
    return mixed % 16777216

def generate_secret_numbers(initial_secret, num_secrets=2000):
    secrets = [initial_secret]
    for _ in range(num_secrets):
        secret = secrets[-1]
        mixed = mix_and_prune(secret, secret * 64)
        mixed = mix_and_prune(mixed, mixed // 32)
        mixed = mix_and_prune(mixed, mixed * 2048)
        secrets.append(mixed)
    return secrets

def get_deltas(secret):
    return [int(str(b)[-1]) - int(str(a)[-1]) for a, b in zip(secret, secret[1:])]

def find_prices(secret):
    deltas = get_deltas(secret)
    prices = {}
    for i in range(len(deltas) - 3):
        sequence = tuple(deltas[i:i+4])
        if 0 not in sequence:
            if sequence not in prices.keys():
                prices[sequence] = int(str(secret[i+4])[-1])
    return prices


with open(getenv("AOC_INPUT", "example_input.txt"), "r") as f:
    secrets = [int(line.strip()) for line in f.readlines()]

secrets = [generate_secret_numbers(secret) for secret in secrets]
print(sum([n[-1] for n in secrets]))

all_prices = [find_prices(s) for s in secrets]
all_sequences = set()
for prices in all_prices:
    all_sequences = all_sequences.union(set(prices.keys()))

res = 0
for sequence in all_sequences:
    total = sum(prices.get(sequence, 0) for prices in all_prices)
    res = max(res, total)
print(res)
