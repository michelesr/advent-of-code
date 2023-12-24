with open("./input") as f:
    lines = [line.strip() for line in f.readlines()]


def count_matches(card) -> int:
    winning, others = card
    matches = [o for o in others if o in winning]
    return len(matches)


cards = []
for line in lines:
    parts = line.split("|")
    winning = parts[0].split(":")[1].split(" ")
    winning = [int(n) for n in winning if n != ""]
    others = parts[1].split(" ")
    others = [int(n) for n in others if n != ""]
    cards.append((winning, others))

final_score = 0
for card in cards:
    num_matches = count_matches(card)
    score = 0
    if num_matches > 0:
        score = 2 ** (num_matches - 1)
    final_score += score

print(final_score)

cards = [[1, card] for card in cards]
for i in range(len(cards)):
    for j in range(count_matches(cards[i][1])):
        cards[i + j + 1][0] += cards[i][0]

print(sum([card[0] for card in cards]))
