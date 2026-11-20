"""Demo for defence, goes by grading criteria. Run: uv run python scripts/demo.py"""

import random
import time

from algopack import (
    EmptyStructureError,
    InputKind,
    InvalidInputError,
    PriorityQueue,
    fib_iterative,
    fib_recursive,
    generate,
    insertion_sort,
    merge_sort,
    quickselect,
)
from algopack.benchmark import measure, run_benchmark
from algopack.consts import MAX_RECURSIVE_N
from algopack.report import to_markdown


def title(text: str) -> None:
    print()
    print("=" * 60)
    print(text)
    print("=" * 60)


def demo_recurrence() -> None:
    title("1. Recurrence: Fibonacci, F(0)=0, F(1)=1")
    print("first 11 iterative:", [fib_iterative(n=n) for n in range(11)])
    print("first 11 recursive:", [fib_recursive(n=n) for n in range(11)])
    print("fib(100) same:", fib_iterative(n=100) == fib_recursive(n=100))

    for bad in (-1, 2.5, "7", True):
        try:
            fib_recursive(n=bad)
        except InvalidInputError as error:
            print(f"bad input {bad!r} ->", error)

    print(f"python recursion limit is about 1000, our limit is {MAX_RECURSIVE_N}")
    try:
        fib_recursive(n=MAX_RECURSIVE_N + 1)
    except InvalidInputError as error:
        print("too deep ->", error)
    print(
        "iterative has no limit, fib(2000) has digits:", len(str(fib_iterative(n=2000)))
    )


def demo_sorts() -> None:
    title("2-3. Sorting: insertion (quadratic) and merge (efficient)")
    sorts = {"insertion_sort": insertion_sort, "merge_sort": merge_sort}
    cases = {
        "empty": [],
        "one item": [5],
        "sorted": [1, 2, 3, 4],
        "reversed": [4, 3, 2, 1],
        "duplicates": [3, 1, 3, 2, 1, 3],
        "negative": [0, -5, 3, -1, -5],
    }
    for name, sort in sorts.items():
        print(f"--- {name}")
        for case_name, data in cases.items():
            print(f"{case_name:>10}: {data} -> {sort(items=data)}")

    print("--- input list is not changed (both sorts return new list)")
    data = [3, 1, 2]
    result = merge_sort(items=data)
    print(
        "input after sort:", data, "| result:", result, "| same object:", data is result
    )

    print("--- wrong type is documented as TypeError")
    for bad in (None, "abc", {3, 1}, [1, "a"]):
        try:
            merge_sort(items=bad)
        except TypeError as error:
            print(f"{bad!r} -> TypeError: {error}")

    print("--- compare with reference sorted() on random lists")
    for seed in range(5):
        rng = random.Random(seed)
        data = [rng.randint(-100, 100) for _ in range(200)]
        same = insertion_sort(items=data) == sorted(data) and merge_sort(
            items=data
        ) == sorted(data)
        print(f"seed {seed}: both equal to sorted():", same)

    print("--- key and stability (equal ages keep original order)")
    people = [("bob", 25), ("ann", 30), ("eve", 25), ("dan", 30), ("kim", 25)]
    for name, sort in sorts.items():
        print(name, sort(items=people, key=lambda p: p[1]))


def demo_priority_queue() -> None:
    title("4. Data structure: priority queue on heap")
    queue: PriorityQueue[str] = PriorityQueue()
    print("empty: len =", len(queue), "| bool =", bool(queue))
    for item, priority in [("write", 3), ("sleep", 5), ("urgent", 1), ("eat", 3)]:
        queue.push(item=item, priority=priority)
    print("after 4 push: len =", len(queue), "| bool =", bool(queue))
    print("peek (not removed):", queue.peek(), "| len =", len(queue))
    print("heap invariant holds:", queue.is_valid_heap())

    order = []
    while queue:
        order.append(queue.pop())
    print("pop order (write and eat have same priority, FIFO):", order)

    for operation in (queue.pop, queue.peek):
        try:
            operation()
        except EmptyStructureError as error:
            print("empty queue ->", error)


def demo_generators() -> None:
    title("5. Generators: five kinds and seed")
    for kind in InputKind:
        print(f"{kind.value:>16}:", generate(kind=kind, size=12, seed=7))

    first = generate(kind=InputKind.RANDOM, size=1000, seed=1)
    second = generate(kind=InputKind.RANDOM, size=1000, seed=1)
    other = generate(kind=InputKind.RANDOM, size=1000, seed=2)
    print("same seed equal:", first == second)
    print("different seed equal:", first == other)


def demo_benchmark() -> None:
    title("6. Benchmark: repeats, sizes, independent copies")
    print("--- why not one mutable list (defence question 3)")
    data = generate(kind=InputKind.RANDOM, size=20_000, seed=1)

    shared = list(data)
    shared_times = []
    for _ in range(5):
        start = time.perf_counter()
        shared.sort()
        shared_times.append(time.perf_counter() - start)
    print("one list sorted in place 5 times, ms:", format_ms(shared_times))
    print("first run sorts it, next runs get already sorted list")

    own_times = measure(func=sort_in_place, data=data, repeats=5)
    print("own copy for each run, ms:          ", format_ms(own_times))

    print("--- small benchmark, sizes 500 1000 2000 (growth shows complexity)")
    rows = run_benchmark(
        sizes=[500, 1000, 2000],
        kinds=[InputKind.RANDOM, InputKind.SORTED],
        repeats=5,
    )
    print(to_markdown(rows=rows))
    print("insertion on random: growth ~4 per 2x size -> O(n^2)")
    print("insertion on sorted: growth ~2 -> O(n), best case")
    print("merge: growth a bit more than 2 -> O(n log n)")


def sort_in_place(items: list[int]) -> None:
    items.sort()


def format_ms(times: list[float]) -> list[str]:
    return [f"{t * 1000:.2f}" for t in times]


def demo_quickselect() -> None:
    title("Extra: quickselect and key")
    data = generate(kind=InputKind.RANDOM, size=15, seed=3)
    ordered = merge_sort(items=data)
    print("data:", data)
    print("sorted:", ordered)
    for k in (0, 7, 14):
        print(f"k={k}:", quickselect(items=data, k=k), "| sorted[k] =", ordered[k])
    words = ["pear", "fig", "banana", "kiwi"]
    print("2nd shortest word:", quickselect(items=words, k=1, key=len))


def main() -> None:
    demo_recurrence()
    demo_sorts()
    demo_priority_queue()
    demo_generators()
    demo_quickselect()
    demo_benchmark()


if __name__ == "__main__":
    main()
