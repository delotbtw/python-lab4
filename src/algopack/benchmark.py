import statistics
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Protocol

from algopack.consts import DEFAULT_REPEATS, DEFAULT_SEED, DEFAULT_SIZES, MIN_REPEATS
from algopack.enums import InputKind
from algopack.errors import InvalidInputError
from algopack.generators import generate
from algopack.sorting import insertion_sort, merge_sort


class SortFunc(Protocol):
    def __call__(self, items: list[int]) -> object: ...


ALGORITHMS: dict[str, SortFunc] = {
    "insertion_sort": insertion_sort,
    "merge_sort": merge_sort,
}


@dataclass(frozen=True)
class BenchmarkRow:
    algorithm: str
    kind: InputKind
    size: int
    repeats: int
    min_s: float
    mean_s: float
    median_s: float


def measure(
    func: SortFunc,
    data: list[int],
    repeats: int,
    timer: Callable[[], float] = time.perf_counter,
) -> list[float]:
    """Time func on own copy of data for each repeat, copy is not timed"""
    if repeats < MIN_REPEATS:
        raise InvalidInputError(message=f"need at least {MIN_REPEATS} repeats")
    times = []
    for _ in range(repeats):
        copy = list(data)
        start = timer()
        func(items=copy)
        times.append(timer() - start)
    return times


def run_benchmark(
    algorithms: dict[str, SortFunc] = ALGORITHMS,
    sizes: Sequence[int] = DEFAULT_SIZES,
    kinds: Sequence[InputKind] = tuple(InputKind),
    repeats: int = DEFAULT_REPEATS,
    seed: int = DEFAULT_SEED,
    timer: Callable[[], float] = time.perf_counter,
) -> list[BenchmarkRow]:
    """Run every algorithm on every kind and size, sizes must go up"""
    rows = []
    for name, func in algorithms.items():
        for kind in kinds:
            for size in sizes:
                data = generate(kind=kind, size=size, seed=seed)
                times = measure(func=func, data=data, repeats=repeats, timer=timer)
                rows.append(
                    BenchmarkRow(
                        algorithm=name,
                        kind=kind,
                        size=size,
                        repeats=repeats,
                        min_s=min(times),
                        mean_s=statistics.fmean(times),
                        median_s=statistics.median(times),
                    )
                )
    return rows
