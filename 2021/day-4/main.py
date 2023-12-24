def check(numbers, board):
    # check rows
    for row in board:
        if set(numbers).issuperset(set(row)):
            return True
    # check columns
    for i in range(len(board[0])):
        col = [row[i] for row in board]
        if set(numbers).issuperset(set(col)):
            return True
    return False

def find_winner(numbers, boards):
    for i in range(5, len(numbers)):
        for board in boards:
            if check(numbers[0:i], board):
                return board, i
    return None, None

def score_board(numbers, board):
    score = 0
    for row in board:
        for n in row:
            if n not in numbers:
                score += int(n)
    return score * int(numbers[-1])

with open("input", "r") as f:
    numbers = f.readline().strip().split(',')

    boards = []
    board = []

    f.readline()

    for l in f.readlines():
        if l == '\n':
            if len(board) > 1:
                boards.append(board)
            board = []
        else:
            board.append(l.strip().replace('  ', ' ').split(' '))


# part 1
winner, last_index = find_winner(numbers, boards)
print(score_board(numbers[0:last_index], winner))

# part 2
while(winner):
    boards.remove(winner)
    prev_last_index = last_index
    prev_winner = winner
    winner, last_index = find_winner(numbers, boards)
print(score_board(numbers[0:prev_last_index], prev_winner))
