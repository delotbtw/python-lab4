import pytest

from algopack import benchmark
from algopack.benchmark import measure, run_benchmark
from algopack.consts import MIN_REPEATS
from algopack.enums import InputKind
from algopack.errors import InvalidInputError


class FakeClock:
    """Time moves only when measured function says so"""

    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def test_repeats_below_minimum_are_rejected():
    with pytest.raises(InvalidInputError):
        measure(func=lambda items: None, data=[1, 2], repeats=MIN_REPEATS - 1)


def test_function_is_called_repeats_times():
    calls = []

    times = measure(
        func=lambda items: calls.append(len(items)),
        data=[1, 2, 3],
        repeats=7,
        timer=FakeClock(),
    )

    assert calls == [3] * 7
    assert len(times) == 7


def test_every_run_gets_own_untouched_copy():
    seen = []

    def mutating(items):
        seen.append(list(items))
        items.clear()

    data = [3, 1, 2]
    measure(func=mutating, data=data, repeats=MIN_REPEATS, timer=FakeClock())

    assert seen == [[3, 1, 2]] * MIN_REPEATS
    assert data == [3, 1, 2]


def test_runs_do_not_share_list_object():
    received = []

    measure(
        func=lambda items: received.append(items),
        data=[1, 2],
        repeats=MIN_REPEATS,
        timer=FakeClock(),
    )

    assert len({id(items) for items in received}) == MIN_REPEATS


def test_timings_come_from_timer():
    clock = FakeClock()

    def work(items):
        clock.now += len(items) * 0.001

    times = measure(func=work, data=[0] * 10, repeats=MIN_REPEATS, timer=clock)

    assert times == pytest.approx([0.01] * MIN_REPEATS)


def test_generation_is_not_inside_timed_part(monkeypatch):
    events = []

    def fake_generate(kind, size, seed):
        events.append("generate")
        return list(range(size))

    def timer():
        events.append("timer")
        return 0.0

    monkeypatch.setattr(benchmark, "generate", fake_generate)
    run_benchmark(
        algorithms={"x": lambda items: events.append("func")},
        sizes=[10],
        kinds=[InputKind.RANDOM],
        timer=timer,
    )

    assert events == ["generate"] + ["timer", "func", "timer"] * MIN_REPEATS


def test_rows_cover_all_algorithms_kinds_and_sizes():
    rows = run_benchmark(
        algorithms={"a": lambda items: None, "b": lambda items: None},
        sizes=[10, 20],
        kinds=[InputKind.RANDOM, InputKind.SORTED],
        timer=FakeClock(),
    )

    assert [(r.algorithm, r.kind, r.size) for r in rows] == [
        (name, kind, size)
        for name in "ab"
        for kind in (InputKind.RANDOM, InputKind.SORTED)
        for size in (10, 20)
    ]
    assert all(row.repeats == MIN_REPEATS for row in rows)


def test_row_has_min_mean_and_median():
    clock = FakeClock()

    def work(items):
        clock.now += 0.5

    rows = run_benchmark(
        algorithms={"x": work}, sizes=[5], kinds=[InputKind.RANDOM], timer=clock
    )

    assert rows[0].min_s == rows[0].mean_s == rows[0].median_s == 0.5


def test_default_run_on_real_algorithms():
    rows = run_benchmark(sizes=[20, 40], kinds=[InputKind.RANDOM])

    assert {row.algorithm for row in rows} == {"insertion_sort", "merge_sort"}
    assert len(rows) == 4
    assert all(row.min_s <= row.median_s for row in rows)
