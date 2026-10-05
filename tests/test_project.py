import random
import tempfile
import unittest
from unittest.mock import patch

from experiments import run_experiments, summarize
from hill_climbing import hill_climbing, hill_climbing_sideways
from random_restart import random_restart_hill_climbing, random_restart_hill_climbing_sideways
from utils import get_neighbors, heuristic


class ProjectTests(unittest.TestCase):
    def test_board_heuristic_and_neighbors(self):
        self.assertEqual(heuristic([1, 3, 0, 2]), 0)
        self.assertEqual(heuristic([0, 0, 0, 0]), 6)
        self.assertEqual(heuristic([0, 1, 2, 3]), 6)
        board = [1, 3, 0, 2]
        neighbors = get_neighbors(board)
        self.assertEqual(len({tuple(b) for b in neighbors}), 12)
        self.assertTrue(all(sum(a != b for a, b in zip(board, other)) == 1
                            for other in neighbors))
        self.assertEqual(board, [1, 3, 0, 2])

    def test_search_invariants(self):
        for seed in range(20):
            for sideways in (False, True):
                random.seed(seed)
                search = hill_climbing_sideways if sideways else hill_climbing
                success, board, steps, path = search(8)
                self.assertEqual(success, heuristic(board) == 0)
                self.assertEqual(path[-1], board)
                self.assertEqual(steps, len(path) - 1)
                for before, after in zip(path, path[1:]):
                    self.assertEqual(sum(a != b for a, b in zip(before, after)), 1)
                    if sideways:
                        self.assertLessEqual(heuristic(after), heuristic(before))
                    else:
                        self.assertLess(heuristic(after), heuristic(before))

    def test_restart_accumulates_failed_attempts(self):
        failed = (False, [0, 0, 0, 0], 1, [[1, 0, 0, 0], [0, 0, 0, 0]])
        solved = (True, [1, 3, 0, 2], 2, [[0, 3, 0, 0], [1, 3, 0, 0], [1, 3, 0, 2]])
        with patch('random_restart.hill_climbing', side_effect=[failed, failed, solved]) as search:
            result = random_restart_hill_climbing(4, initial_board=[1, 0, 0, 0])
            self.assertEqual(result[:4], (True, solved[1], 4, 2))
            self.assertEqual(len(result[4]), 3)
            self.assertIsNone(search.call_args.kwargs['initial_board'])
        with patch('random_restart.hill_climbing', return_value=failed) as search:
            result = random_restart_hill_climbing(4, max_restarts=1)
            self.assertFalse(result[0])
            self.assertEqual(result[2:4], (2, 1))
            self.assertEqual(search.call_count, 2)

    def test_sideways_integration_and_limits(self):
        solved = (True, [1, 3, 0, 2], 0, [[1, 3, 0, 2]])
        with patch('random_restart.hill_climbing_sideways', return_value=solved) as search:
            result = random_restart_hill_climbing_sideways(4, max_sideways=7)
            self.assertEqual(result[3], 0)
            self.assertEqual(search.call_args.kwargs['max_sideways'], 7)
        for n in (0, 2, 3):
            with self.assertRaises(ValueError):
                random_restart_hill_climbing(n)
        self.assertTrue(random_restart_hill_climbing(1)[0])

    def test_statistics_and_reproducibility(self):
        records = [dict(algorithm='test', success=True, steps=2, restarts=0),
                   dict(algorithm='test', success=False, steps=4, restarts=2)]
        stats = summarize(records)
        self.assertEqual(stats['success_rate_pct'], 50)
        self.assertEqual(stats['avg_steps'], 3)
        self.assertEqual(stats['avg_steps_success'], 2)
        self.assertEqual(stats['avg_steps_failure'], 4)
        self.assertIsNone(summarize(records[:1])['avg_steps_failure'])
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            self.assertEqual(run_experiments(n=4, output_dir=first, trial_counts=(3,)),
                             run_experiments(n=4, output_dir=second, trial_counts=(3,)))


if __name__ == '__main__':
    unittest.main()
