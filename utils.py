import random


def random_board(n):
    """
    Generate a random N-Queens board.

    Board representation:
    the index is the column and the value is the row
    containing the queen.
    """
    board = []

    for column in range(n):
        row = random.randint(0, n - 1)
        board.append(row)

    return board


def heuristic(board):
    """
    Return the number of pairs of queens attacking each other.
    A solution has a heuristic value of 0.
    """
    conflicts = 0
    n = len(board)

    for i in range(n):
        for j in range(i + 1, n):

            # Queens in the same row
            if board[i] == board[j]:
                conflicts += 1

            # Queens on the same diagonal
            elif abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def get_neighbors(board):
    """
    Generate all neighboring states by moving one queen
    to another row in its current column.
    """
    neighbors = []
    n = len(board)

    for column in range(n):
        for row in range(n):

            if row != board[column]:
                new_board = board.copy()
                new_board[column] = row
                neighbors.append(new_board)

    return neighbors