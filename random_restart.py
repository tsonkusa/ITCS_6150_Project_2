"""Restart wrappers; paths are grouped by attempt to preserve restart boundaries."""

from hill_climbing import hill_climbing, hill_climbing_sideways


def _restart(search, n, max_restarts, initial_board):
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    if n in (2, 3):
        raise ValueError("N=2 and N=3 have no solutions")
    if max_restarts is not None and (
        not isinstance(max_restarts, int) or isinstance(max_restarts, bool)
        or max_restarts < 0
    ):
        raise ValueError("max_restarts must be a nonnegative integer or None")

    total_steps = 0
    restarts = 0
    paths = []
    while True:
        success, board, steps, path = search(n, initial_board=initial_board)
        total_steps += steps
        paths.append(path)
        if success or (max_restarts is not None and restarts >= max_restarts):
            return success, board, total_steps, restarts, paths
        restarts += 1
        initial_board = None


def random_restart_hill_climbing(n, max_restarts=None, initial_board=None):
    """Return (success, board, total_steps, restarts, attempt_paths).

    The initial attempt is not a restart. None means retry until solved.
    Steps count queen moves across all attempts, excluding board resets.
    """
    return _restart(hill_climbing, n, max_restarts, initial_board)


def random_restart_hill_climbing_sideways(
    n, max_sideways=100, max_restarts=None, initial_board=None
):
    """Restart hill climbing with a consecutive sideways limit per attempt."""
    if not isinstance(max_sideways, int) or isinstance(max_sideways, bool) or max_sideways < 0:
        raise ValueError("max_sideways must be a nonnegative integer")

    def search(size, initial_board=None):
        return hill_climbing_sideways(
            size, max_sideways=max_sideways, initial_board=initial_board
        )

    return _restart(search, n, max_restarts, initial_board)
