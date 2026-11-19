import csv
import io
from collections.abc import Sequence
from pathlib import Path

from algopack.benchmark import BenchmarkRow
from algopack.consts import EXPECTED_COMPLEXITY, SECONDS_TO_MS

HEADER = (
    "algorithm",
    "input",
    "size",
    "repeats",
    "min_ms",
    "mean_ms",
    "median_ms",
    "growth",
    "expected",
)


def _table(rows: Sequence[BenchmarkRow]) -> list[list[str]]:
    """Rows as strings, growth is mean time / mean time of previous size"""
    previous: dict[tuple[str, str], float] = {}
    table = []
    for row in rows:
        key = (row.algorithm, row.kind.value)
        before = previous.get(key)
        growth = f"{row.mean_s / before:.1f}" if before else ""
        previous[key] = row.mean_s
        expected = EXPECTED_COMPLEXITY.get(row.algorithm)
        table.append(
            [
                row.algorithm,
                row.kind.value,
                str(row.size),
                str(row.repeats),
                f"{row.min_s * SECONDS_TO_MS:.3f}",
                f"{row.mean_s * SECONDS_TO_MS:.3f}",
                f"{row.median_s * SECONDS_TO_MS:.3f}",
                growth,
                expected.value if expected else "",
            ]
        )
    return table


def to_csv(rows: Sequence[BenchmarkRow]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(_table(rows=rows))
    return buffer.getvalue()


def to_markdown(rows: Sequence[BenchmarkRow]) -> str:
    lines = ["# Benchmark report", "", "| " + " | ".join(HEADER) + " |"]
    lines.append("|" + "---|" * len(HEADER))
    for cells in _table(rows=rows):
        lines.append("| " + " | ".join(cells) + " |")
    lines += ["", "growth: how many times mean time grew from the previous size", ""]
    return "\n".join(lines)


def write_reports(rows: Sequence[BenchmarkRow], directory: Path) -> None:
    """Save benchmark.csv and benchmark.md"""
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "benchmark.csv").write_text(to_csv(rows=rows), encoding="utf-8")
    (directory / "benchmark.md").write_text(to_markdown(rows=rows), encoding="utf-8")
