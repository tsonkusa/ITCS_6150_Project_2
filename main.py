from utils import random_board
from utils import heuristic
from utils import get_neighbors

from hill_climbing import hill_climbing
from hill_climbing import hill_climbing_sideways


print("TEST 1: Random board")
board = random_board(8)
print("Board:", board)
print("Length:", len(board))
print()


print("TEST 2: Heuristic with known solution")
solution = [0, 4, 7, 5, 2, 6, 1, 3]
print("Board:", solution)
print("Heuristic:", heuristic(solution))
print()


print("TEST 3: Heuristic with conflicting board")
bad_board = [0, 0, 0, 0]
print("Board:", bad_board)
print("Heuristic:", heuristic(bad_board))
print()


print("TEST 4: Neighbor generation")
board = random_board(8)
neighbors = get_neighbors(board)

print("Board:", board)
print("Number of neighbors:", len(neighbors))
print()


print("TEST 5: Normal Hill Climbing")
success, final_board, steps, path = hill_climbing(8)

print("Success:", success)
print("Final board:", final_board)
print("Final heuristic:", heuristic(final_board))
print("Steps:", steps)
print("Path length:", len(path))
print()


print("TEST 6: Hill Climbing with Sideways Moves")
success, final_board, steps, path = hill_climbing_sideways(8)

print("Success:", success)
print("Final board:", final_board)
print("Final heuristic:", heuristic(final_board))
print("Steps:", steps)
print("Path length:", len(path))
print()