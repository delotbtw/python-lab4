import argparse
from collections.abc import Sequence
from pathlib import Path

from algopack.benchmark import run_benchmark
from algopack.consts import DEFAULT_REPEATS, DEFAULT_SEED, DEFAULT_SIZES
from algopack.report import write_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run sort benchmark, save reports")
    parser.add_argument("--sizes", type=int, nargs="+", default=list(DEFAULT_SIZES))
    parser.add_argument("--repeats", type=int, default=DEFAULT_REPEATS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=Path("reports"))
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    rows = run_benchmark(sizes=args.sizes, repeats=args.repeats, seed=args.seed)
    write_reports(rows=rows, directory=args.out)
    print(f"saved reports to {args.out}")
