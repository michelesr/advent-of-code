from collections import Counter
from typing import Collection
from functools import cmp_to_key


def get_card_value(card, part_two=False) -> int:
    deck = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    if part_two:
        deck = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    deck = list(reversed(deck))
    return deck.index(card)


def get_hand_value(hand: Collection[str], part_two=False) -> int:
    h = Counter(hand)
    jokers = 0
    if part_two and "J" in hand:
        jokers = h["J"]
        if jokers == 5:
            # 5 of a kind
            return 20
        del h["J"]
    vals = h.values()
    m = max(vals)
    # 5 of a kind
    if m == 5:
        res = 20
    # 4 of a kind
    elif m == 4:
        res = 19
        if part_two and "J" in hand:
            # 5 of a kind
            res = 20
    # full house
    elif 3 in vals and 2 in vals:
        res = 18
        if part_two and "J" in hand:
            if jokers == 1:
                # 4 of a kind
                res = 19
                # 5 of a kind
            elif h["J"] == 2:
                res = 20
    # 3 of a kind
    elif 3 in vals:
        res = 17
        if part_two and "J" in hand:
            if jokers == 1:
                # 4 of a kind
                res = 19
            elif jokers == 2:
                # 5 of a kind
                res = 20
    # two pairs
    elif len([v for v in vals if v == 2]) == 2:
        res = 16
        if part_two and "J" in hand:
            if jokers == 1:
                # full house
                res = 18
            elif jokers == 2:
                # 5 of a kind
                res = 20
    # one pair
    elif 2 in vals:
        res = 15
        if part_two and "J" in hand:
            if jokers == 1:
                # 3 of a kind
                res = 17
            elif jokers == 2:
                # 4 of a kind
                res = 19
            elif jokers == 3:
                # 5 of a kind
                res = 20
    # high card
    else:
        res = 14
        if part_two and "J" in hand:
            if jokers == 1:
                # one pair
                res = 15
            if jokers == 2:
                # 3 of a kind
                res = 17
            elif jokers == 3:
                # 4 of a kind
                res = 19
            elif jokers == 4:
                # 5 of a kind
                res = 20
    return res


def compare_hand(a, b, part_two=False):
    if get_hand_value(a, part_two) < get_hand_value(b, part_two):
        return -1
    elif get_hand_value(a, part_two) > get_hand_value(b, part_two):
        return 1
    else:
        for i in range(len(a)):
            if get_card_value(a[i], part_two) < get_card_value(b[i], part_two):
                return -1
            elif get_card_value(a[i], part_two) > get_card_value(b[i], part_two):
                return 1
        raise ValueError("Hands are equal!")


hands = []
with open("./input") as f:
    for line in f.readlines():
        parts = line.strip().split(" ")
        cards = list(parts[0])
        rank = int(parts[1])
        hands.append((cards, rank))

# part one
old_hands = hands.copy()
hands.sort(key=cmp_to_key(lambda a, b: compare_hand(a[0], b[0])))
res = 0
for i in range(len(hands)):
    res += hands[i][1] * (i + 1)
print(res)

# part two
hands = old_hands
hands.sort(key=cmp_to_key(lambda a, b: compare_hand(a[0], b[0], part_two=True)))
res = 0
for i in range(len(hands)):
    res += hands[i][1] * (i + 1)
print(res)
