from enum import Enum
from functools import reduce


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6


def parse(shape):
    map = {
        "A": Shape.ROCK,
        "B": Shape.PAPER,
        "C": Shape.SCISSORS,
        "X": Shape.ROCK,
        "Y": Shape.PAPER,
        "Z": Shape.SCISSORS,
    }
    return map[shape]


def score_part_one(round):
    map = {
        (Shape.ROCK, Shape.ROCK): Result.DRAW,
        (Shape.ROCK, Shape.PAPER): Result.WIN,
        (Shape.ROCK, Shape.SCISSORS): Result.LOSS,
        (Shape.PAPER, Shape.ROCK): Result.LOSS,
        (Shape.PAPER, Shape.PAPER): Result.DRAW,
        (Shape.PAPER, Shape.SCISSORS): Result.WIN,
        (Shape.SCISSORS, Shape.ROCK): Result.WIN,
        (Shape.SCISSORS, Shape.PAPER): Result.LOSS,
        (Shape.SCISSORS, Shape.SCISSORS): Result.DRAW,
    }
    return map[round].value + round[1].value


def convert(round):
    map = {
        Shape.ROCK: Result.LOSS,
        Shape.PAPER: Result.DRAW,
        Shape.SCISSORS: Result.WIN,
    }
    return (round[0], map[round[1]])


def find_shape(round):
    map = {
        (Shape.ROCK, Result.LOSS): Shape.SCISSORS,
        (Shape.ROCK, Result.DRAW): Shape.ROCK,
        (Shape.ROCK, Result.WIN): Shape.PAPER,
        (Shape.PAPER, Result.LOSS): Shape.ROCK,
        (Shape.PAPER, Result.DRAW): Shape.PAPER,
        (Shape.PAPER, Result.WIN): Shape.SCISSORS,
        (Shape.SCISSORS, Result.LOSS): Shape.PAPER,
        (Shape.SCISSORS, Result.DRAW): Shape.SCISSORS,
        (Shape.SCISSORS, Result.WIN): Shape.ROCK,
    }
    return map[round]


def score_part_two(round):
    return round[1].value + find_shape(round).value


with open("input", "r") as f:
    rounds = [
        tuple(map(parse, line.replace("\n", "").split(" "))) for line in f.readlines()
    ]

# part one
print(reduce(lambda x, y: x + score_part_one(y), rounds, 0))

# part two
rounds = tuple(map(convert, rounds))
print(reduce(lambda x, y: x + score_part_two(y), rounds, 0))
