import random
from collections.abc import Callable

from algopack.consts import (
    DEFAULT_SEED,
    DUPLICATE_DISTINCT_VALUES,
    NEARLY_SORTED_SWAP_RATIO,
    VALUE_LIMIT,
)
from algopack.enums import InputKind
from algopack.errors import InvalidInputError
from algopack.sorting import merge_sort


def _check_args(size: int, seed: int) -> None:
    for name, value in (("size", size), ("seed", seed)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise InvalidInputError(message=f"{name} must be int: {value!r}")
    if size < 0:
        raise InvalidInputError(message=f"size must be non negative: {size}")


def random_list(size: int, seed: int = DEFAULT_SEED) -> list[int]:
    """Random ints, can be negative"""
    _check_args(size=size, seed=seed)
    rng = random.Random(seed)
    return [rng.randint(-VALUE_LIMIT, VALUE_LIMIT) for _ in range(size)]


def sorted_list(size: int, seed: int = DEFAULT_SEED) -> list[int]:
    """Random ints in ascending order"""
    return merge_sort(items=random_list(size=size, seed=seed))


def reversed_list(size: int, seed: int = DEFAULT_SEED) -> list[int]:
    """Random ints in descending order"""
    return sorted_list(size=size, seed=seed)[::-1]


def nearly_sorted_list(size: int, seed: int = DEFAULT_SEED) -> list[int]:
    """Sorted list with few random swaps"""
    data = sorted_list(size=size, seed=seed)
    if size < 2:
        return data
    rng = random.Random(seed + 1)
    for _ in range(max(1, int(size * NEARLY_SORTED_SWAP_RATIO))):
        i, j = rng.randrange(size), rng.randrange(size)
        data[i], data[j] = data[j], data[i]
    return data


def many_duplicates_list(size: int, seed: int = DEFAULT_SEED) -> list[int]:
    """Ints from small set of values, so many equal items"""
    _check_args(size=size, seed=seed)
    rng = random.Random(seed)
    low = -(DUPLICATE_DISTINCT_VALUES // 2)
    high = low + DUPLICATE_DISTINCT_VALUES - 1
    return [rng.randint(low, high) for _ in range(size)]


GENERATORS: dict[InputKind, Callable[..., list[int]]] = {
    InputKind.RANDOM: random_list,
    InputKind.SORTED: sorted_list,
    InputKind.REVERSED: reversed_list,
    InputKind.NEARLY_SORTED: nearly_sorted_list,
    InputKind.MANY_DUPLICATES: many_duplicates_list,
}


def generate(kind: InputKind, size: int, seed: int = DEFAULT_SEED) -> list[int]:
    """Make new list of given kind, same seed gives same list"""
    return GENERATORS[kind](size=size, seed=seed)
