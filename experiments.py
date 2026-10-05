"""Reproducible independent experiments and human-readable search traces."""

import csv
import json
import random
from pathlib import Path
from statistics import mean

from hill_climbing import hill_climbing, hill_climbing_sideways
from random_restart import (
    random_restart_hill_climbing,
    random_restart_hill_climbing_sideways,
)
from utils import heuristic, random_board

TRIAL_COUNTS = (50, 100, 200, 500, 1000, 1500)
ALGORITHMS = (
    "Hill Climbing", "Hill Climbing with Sideways",
    "Random Restart", "Random Restart with Sideways",
)


def run_algorithm(index, n, max_sideways, max_restarts, initial_board=None):
    if index == 0:
        success, board, steps, path = hill_climbing(n, initial_board=initial_board)
        return success, board, steps, 0, [path]
    if index == 1:
        success, board, steps, path = hill_climbing_sideways(n, max_sideways, initial_board=initial_board)
        return success, board, steps, 0, [path]
    if index == 2:
        return random_restart_hill_climbing(n, max_restarts=max_restarts)
    return random_restart_hill_climbing_sideways(
        n, max_sideways=max_sideways, max_restarts=max_restarts
    )


def average(records, key):
    return mean(record[key] for record in records) if records else None


def summarize(records):
    successes = [record for record in records if record["success"]]
    failures = [record for record in records if not record["success"]]
    return {
        "algorithm": records[0]["algorithm"],
        "trials": len(records),
        "successes": len(successes),
        "failures": len(failures),
        "success_rate_pct": 100 * len(successes) / len(records),
        "failure_rate_pct": 100 * len(failures) / len(records),
        "avg_steps": average(records, "steps"),
        "avg_steps_success": average(successes, "steps"),
        "avg_steps_failure": average(failures, "steps"),
        "avg_restarts": average(records, "restarts"),
        "avg_restarts_success": average(successes, "restarts"),
        "avg_restarts_failure": average(failures, "restarts"),
    }


def write_csv(path, records):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def run_experiments(n=8, seed=6150, max_sideways=100, max_restarts=None,
                    output_dir="report", trial_counts=TRIAL_COUNTS):
    if not isinstance(n, int) or isinstance(n, bool) or n < 1 or n in (2, 3):
        raise ValueError("Use N=1 or N>=4")
    if max_sideways < 0 or (max_restarts is not None and max_restarts < 0):
        raise ValueError("Move and restart limits must be nonnegative")
    if not trial_counts or any(count < 1 for count in trial_counts):
        raise ValueError("Trial counts must be positive")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    summaries, raw, examples = [], [], {}
    saved_random_state = random.getstate()
    try:
        for count in trial_counts:
            for index, name in enumerate(ALGORITHMS):
                batch = []
                for trial in range(1, count + 1):
                    # A unique deterministic stream for every run; batches are independent.
                    trial_seed = seed + count * 1_000_000 + index * 100_000 + trial
                    random.seed(trial_seed)
                    success, board, steps, restarts, paths = run_algorithm(
                        index, n, max_sideways, max_restarts
                    )
                    record = {
                        "algorithm": name, "batch_trials": count, "trial": trial,
                        "seed": trial_seed, "success": success, "steps": steps,
                        "restarts": restarts, "final_heuristic": heuristic(board),
                        "final_board": json.dumps(board),
                    }
                    batch.append(record)
                    raw.append(record)
                summaries.append(summarize(batch))
                print(f"Completed {name}: {count} trials", flush=True)
        # Four independent random boards, shared by the two single-run algorithms.
        for configuration in range(1, 5):
            board_seed = seed + 10_000_000_000 + configuration
            random.seed(board_seed)
            initial_board = random_board(n)
            for index in (0, 1):
                search_seed = board_seed + (index + 1) * 100_000
                random.seed(search_seed)
                success, board, steps, restarts, paths = run_algorithm(
                    index, n, max_sideways, max_restarts, initial_board
                )
                name = f"{ALGORITHMS[index]}: configuration {configuration}"
                examples[name] = {
                    "initial_board": initial_board, "board_seed": board_seed,
                    "seed": search_seed, "success": success, "steps": steps,
                    "restarts": restarts, "final_board": board, "attempt_paths": paths,
                }
    finally:
        random.setstate(saved_random_state)

    metadata = {
        "n": n, "base_seed": seed, "max_sideways": max_sideways,
        "max_restarts": max_restarts, "trial_counts": list(trial_counts),
        "batch_design": "Independent batches; independent seed per algorithm/trial",
        "steps": "Queen moves across all attempts; resets are excluded",
        "restarts": "Attempts after the initial attempt",
        "rates": "Percent of complete trials, not individual restart attempts",
        "missing_averages": "No observations in the success/failure group",
    }
    write_csv(output / "results.csv", summaries)
    write_csv(output / "trials.csv", raw)
    (output / "experiment_config.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (output / "search_sequences.json").write_text(json.dumps(examples, indent=2) + "\n")
    write_tables(output, summaries, metadata)
    write_sequences(output, examples, n)
    return summaries


def formatted(value):
    return "N/A" if value is None else f"{value:.2f}"


def write_tables(output, summaries, metadata):
    lines = ["# Experiment Results", "", f"N={metadata['n']}; base seed={metadata['base_seed']}; "
             f"sideways limit={metadata['max_sideways']} consecutive moves.", "",
             f"Restart limit: {metadata['max_restarts'] if metadata['max_restarts'] is not None else 'unlimited (until success)' }.", "",
             "Each trial count is an independent batch. Steps count queen moves across all "
             "attempts; restarts exclude the initial attempt. Rates measure complete trials. "
             "Unlimited restart runs continue until solved, so their 100% success is a "
             "consequence of the stopping rule. N/A means the group has no observations.", ""]
    for name in ALGORITHMS:
        lines += [f"## {name}", "",
                  "| Trials | Successes | Failures | Success % | Failure % | Avg steps (all) | Avg steps (success) | Avg steps (failure) | Avg restarts (all) | Avg restarts (success) | Avg restarts (failure) |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]
        for row in summaries:
            if row["algorithm"] == name:
                values = [str(row[key]) for key in ("trials", "successes", "failures")]
                values += [formatted(row[key]) for key in (
                    "success_rate_pct", "failure_rate_pct", "avg_steps", "avg_steps_success",
                    "avg_steps_failure", "avg_restarts", "avg_restarts_success", "avg_restarts_failure")]
                lines.append("| " + " | ".join(values) + " |")
        lines.append("")
    (output / "results.md").write_text("\n".join(lines) + "\n")


def write_sequences(output, examples, n):
    lines = ["# Search Sequences", "", "Rows and columns are zero-based. Q marks a queen; "
             "h counts attacking pairs. Each restart begins a separate attempt; resets "
             "are not counted as moves. Four random initial boards are shared by the two single-run algorithms.", ""]
    for name, example in examples.items():
        lines += [f"## {name}", "", f"Success: {example['success']}; seed: {example['seed']}; steps: {example['steps']}; "
                  f"restarts: {example['restarts']}.", ""]
        for attempt, path in enumerate(example["attempt_paths"], 1):
            lines += [f"### Attempt {attempt}", ""]
            for move, board in enumerate(path):
                lines += [f"Move {move}: `{board}`, h={heuristic(board)}", "", "```text"]
                lines += [" ".join("Q" if board[column] == row else "."
                                    for column in range(n)) for row in range(n)]
                lines += ["```", ""]
    (output / "search_sequences.md").write_text("\n".join(lines) + "\n")
