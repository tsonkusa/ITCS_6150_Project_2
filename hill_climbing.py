import random

from utils import random_board
from utils import heuristic
from utils import get_neighbors


def hill_climbing(n, initial_board=None):
    """
    Standard hill-climbing search for the N-Queens problem.

    Returns:
        success: True if a solution is found, otherwise False
        final_board: the final board reached
        steps: number of moves made
        path: list of all states visited
    """

    if initial_board is None:
        current = random_board(n)
    else:
        current = initial_board.copy()

    path = [current.copy()]
    steps = 0

    while True:

        current_h = heuristic(current)

        # Goal found
        if current_h == 0:
            return True, current, steps, path

        neighbors = get_neighbors(current)

        best_h = current_h
        best_neighbors = []

        for neighbor in neighbors:

            h = heuristic(neighbor)

            if h < best_h:
                best_h = h
                best_neighbors = [neighbor]

            elif h == best_h and h < current_h:
                best_neighbors.append(neighbor)

        # No better neighbor exists
        if len(best_neighbors) == 0:
            return False, current, steps, path

        # Choose randomly if there are multiple best neighbors
        current = random.choice(best_neighbors)

        steps += 1
        path.append(current.copy())


def hill_climbing_sideways(n, max_sideways=100, initial_board=None):
    """
    Hill-climbing search with sideways moves.

    Sideways moves allow the algorithm to move to a state
    with the same heuristic value.

    max_sideways limits the number of consecutive sideways
    moves so the algorithm does not continue forever.

    Returns:
        success: True if a solution is found, otherwise False
        final_board: the final board reached
        steps: number of moves made
        path: list of all states visited
    """

    if initial_board is None:
        current = random_board(n)
    else:
        current = initial_board.copy()

    path = [current.copy()]
    steps = 0
    sideways_moves = 0

    while True:

        current_h = heuristic(current)

        # Goal found
        if current_h == 0:
            return True, current, steps, path

        neighbors = get_neighbors(current)

        best_h = None
        best_neighbors = []

        for neighbor in neighbors:

            h = heuristic(neighbor)

            if best_h is None or h < best_h:
                best_h = h
                best_neighbors = [neighbor]

            elif h == best_h:
                best_neighbors.append(neighbor)

        # All neighboring states are worse
        if best_h > current_h:
            return False, current, steps, path

        # Better move
        if best_h < current_h:

            current = random.choice(best_neighbors)

            sideways_moves = 0
            steps += 1

            path.append(current.copy())

        # Sideways move
        elif best_h == current_h:

            if sideways_moves >= max_sideways:
                return False, current, steps, path

            current = random.choice(best_neighbors)

            sideways_moves += 1
            steps += 1

            path.append(current.copy())