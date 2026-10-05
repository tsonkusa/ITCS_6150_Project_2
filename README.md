# Programming Project 2

## Team Members
- Tarang Sonkusare
- Janmesh Shroff

## Description
Implementation of the N-Queens problem using:
- Hill Climbing
- Hill Climbing with Sideways Moves
- Random Restart Hill Climbing

Language: Python

## Project Structure
```text
ITCS_6150_Project_2/
├── main.py
├── hill_climbing.py
├── random_restart.py
├── utils.py
├── experiments.py
├── report/
├── README.md
└── requirements.txt
```

## Running the Experiments

Requires Python 3. No external packages are needed.

```sh
python3 main.py
```

The default run uses N=8 and independent batches of 50, 100, 200, 500,
1000, and 1500 trials for each of the four algorithms. The sideways limit
is 100 consecutive moves; an improving move resets that counter.

To choose N or configure the run:

```sh
python3 main.py --n 10 --seed 6150 --max-sideways 100 --output-dir report_n10
```

N must be 1 or at least 4; N=2 and N=3 have no solution. Random restart
continues until success by default. Use `--max-restarts 100` to cap it at
100 restarts (101 attempts) per trial. Unlimited runs have no fixed runtime
bound. The required assignment results use N=8.

## Results and Search Sequences

Generated files in `report/`:

- `results.md`: readable tables for all four algorithms and six trial counts.
- `results.csv`: unrounded aggregate statistics.
- `trials.csv`: per-trial seeds, outcomes, steps, restarts, and final boards.
- `experiment_config.json`: experiment settings and measurement definitions.
- `search_sequences.md`: complete board-by-board sequences for four random
  initial configurations for Hill Climbing and four for Hill Climbing with
  Sideways Moves. Both algorithms use the same four starting configurations.
- `search_sequences.json`: machine-readable sequences and seeds.

Success/failure rates measure complete trials. Steps are queen moves,
including moves in failed restart attempts; generating a new board is not
counted as a move. Restarts count attempts after the initial attempt. Tables
report average steps and restarts over all trials and separately over successful
and failed trials. N/A indicates a group with no observations. Unlimited
random restart stops only on success, so its success rate is 100% by design;
its average effort is the meaningful comparison.

Batches are independent rather than cumulative. Each trial has its own
recorded seed for repeatability in the same Python/code environment. Restart
functions return `(success, final_board, total_steps, restarts, attempt_paths)`;
paths are grouped by attempt so board resets remain explicit. The original
hill-climbing functions retain their four-value return format.

## Validation

```sh
python3 -m unittest discover -s tests -v
```

Checks cover queen conflicts and neighbors, search-path invariants, restart
accounting and limits, sideways integration, summary statistics, and reproducibility.
