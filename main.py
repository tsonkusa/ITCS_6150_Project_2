"""Command-line entry point for the required experiment batches."""

import argparse
from experiments import run_experiments


def main():
    parser = argparse.ArgumentParser(description="Run N-Queens experiments")
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--seed", type=int, default=6150)
    parser.add_argument("--max-sideways", type=int, default=100)
    parser.add_argument("--max-restarts", type=int, default=None,
                        help="Restart cap; omit to retry until solved")
    parser.add_argument("--output-dir", default="report")
    args = parser.parse_args()
    run_experiments(n=args.n, seed=args.seed, max_sideways=args.max_sideways,
                    max_restarts=args.max_restarts, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
