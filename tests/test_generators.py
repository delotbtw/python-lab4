import itertools

import pytest

from algopack.consts import DUPLICATE_DISTINCT_VALUES
from algopack.enums import InputKind
from algopack.errors import InvalidInputError
from algopack.generators import generate

KINDS = list(InputKind)


def is_non_decreasing(data):
    return all(a <= b for a, b in itertools.pairwise(data))


@pytest.mark.parametrize("kind", KINDS)
def test_same_seed_gives_same_list(kind):
    assert generate(kind=kind, size=200, seed=5) == generate(
        kind=kind, size=200, seed=5
    )


@pytest.mark.parametrize("kind", KINDS)
def test_different_seeds_give_different_lists(kind):
    assert generate(kind=kind, size=200, seed=1) != generate(
        kind=kind, size=200, seed=2
    )


@pytest.mark.parametrize("kind", KINDS)
def test_default_seed_is_reproducible(kind):
    assert generate(kind=kind, size=50) == generate(kind=kind, size=50)


@pytest.mark.parametrize("kind", KINDS)
@pytest.mark.parametrize("size", [0, 1, 2, 10, 123])
def test_size_is_respected(kind, size):
    assert len(generate(kind=kind, size=size, seed=3)) == size


@pytest.mark.parametrize("kind", KINDS)
def test_returns_new_list_every_time(kind):
    first = generate(kind=kind, size=10)
    second = generate(kind=kind, size=10)

    first.append(1)

    assert first is not second
    assert len(second) == 10


def test_sorted_kind_is_sorted():
    assert is_non_decreasing(generate(kind=InputKind.SORTED, size=300, seed=1))


def test_reversed_kind_is_reversed():
    data = generate(kind=InputKind.REVERSED, size=300, seed=1)

    assert is_non_decreasing(data[::-1])
    assert data != data[::-1]


def test_nearly_sorted_is_close_but_not_sorted():
    data = generate(kind=InputKind.NEARLY_SORTED, size=1000, seed=1)
    base = generate(kind=InputKind.SORTED, size=1000, seed=1)
    moved = sum(a != b for a, b in zip(data, base, strict=True))

    assert not is_non_decreasing(data)
    assert moved <= 2 * 50
    assert sorted(data) == base


def test_many_duplicates_has_few_distinct_values():
    data = generate(kind=InputKind.MANY_DUPLICATES, size=1000, seed=1)

    assert len(set(data)) <= DUPLICATE_DISTINCT_VALUES


def test_random_has_negative_numbers():
    assert any(x < 0 for x in generate(kind=InputKind.RANDOM, size=200, seed=1))


@pytest.mark.parametrize("kind", KINDS)
@pytest.mark.parametrize("size", [-1, 1.5, "10", None, True])
def test_bad_size_raises(kind, size):
    with pytest.raises(InvalidInputError):
        generate(kind=kind, size=size)


@pytest.mark.parametrize("kind", KINDS)
def test_bad_seed_raises(kind):
    with pytest.raises(InvalidInputError):
        generate(kind=kind, size=10, seed="x")
