import random


def random_board(n):
    board = []

    for column in range(n):
        row = random.randint(0, n - 1)
        board.append(row)

    return board


def heuristic(board):
    conflicts = 0
    n = len(board)

    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                conflicts += 1
            elif abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def get_neighbors(board):
    neighbors = []
    n = len(board)
    for column in range(n):
        for row in range(n):
            if row != board[column]:
                new_board = board.copy()
                new_board[column] = row
                neighbors.append(new_board)
    return neighbors