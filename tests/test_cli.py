from pathlib import Path

from algopack.cli import build_parser
from algopack.consts import DEFAULT_REPEATS, DEFAULT_SEED, DEFAULT_SIZES


def test_parser_defaults():
    args = build_parser().parse_args([])

    assert tuple(args.sizes) == DEFAULT_SIZES
    assert args.repeats == DEFAULT_REPEATS
    assert args.seed == DEFAULT_SEED
    assert args.out == Path("reports")


def test_parser_reads_options():
    args = build_parser().parse_args(
        ["--sizes", "10", "20", "--repeats", "6", "--seed", "1", "--out", "x"]
    )

    assert args.sizes == [10, 20]
    assert args.repeats == 6
    assert args.seed == 1
    assert args.out == Path("x")
