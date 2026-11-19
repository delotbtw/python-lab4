import csv
import io

import pytest

from algopack.benchmark import BenchmarkRow
from algopack.enums import InputKind
from algopack.report import HEADER, to_csv, to_markdown


def make_row(size, mean_s, algorithm="merge_sort", kind=InputKind.RANDOM):
    return BenchmarkRow(
        algorithm=algorithm,
        kind=kind,
        size=size,
        repeats=5,
        min_s=mean_s,
        mean_s=mean_s,
        median_s=mean_s,
    )


@pytest.fixture
def rows():
    return [
        make_row(size=100, mean_s=0.001),
        make_row(size=1000, mean_s=0.013),
        make_row(size=100, mean_s=0.002, kind=InputKind.SORTED),
    ]


def test_csv_has_header_and_row_for_each_result(rows):
    parsed = list(csv.reader(io.StringIO(to_csv(rows=rows))))

    assert tuple(parsed[0]) == HEADER
    assert len(parsed) == 1 + len(rows)
    assert parsed[1][:4] == ["merge_sort", "random", "100", "5"]


def test_growth_is_relative_to_previous_size_of_same_input(rows):
    parsed = list(csv.DictReader(io.StringIO(to_csv(rows=rows))))

    assert [row["growth"] for row in parsed] == ["", "13.0", ""]


def test_expected_complexity_is_in_report(rows):
    parsed = list(csv.DictReader(io.StringIO(to_csv(rows=rows))))

    assert parsed[0]["expected"] == "O(n log n)"


def test_markdown_has_table(rows):
    text = to_markdown(rows=rows)

    assert text.startswith("# Benchmark report")
    assert "| algorithm | input | size |" in text
    assert "| merge_sort | random | 1000 |" in text
