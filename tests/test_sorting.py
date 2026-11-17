import itertools

import pytest

from algopack.sorting import insertion_sort
from tests.helpers import random_list

SORTS = [insertion_sort]


@pytest.mark.parametrize("sort", SORTS)
def test_empty_list(sort):
    assert sort(items=[]) == []


@pytest.mark.parametrize("sort", SORTS)
def test_single_item(sort):
    assert sort(items=[7]) == [7]


@pytest.mark.parametrize("sort", SORTS)
def test_sorted_and_reversed_input(sort):
    data = list(range(20))

    assert sort(items=data) == data
    assert sort(items=data[::-1]) == data


@pytest.mark.parametrize("sort", SORTS)
def test_duplicates(sort):
    assert sort(items=[3, 1, 3, 2, 1, 3, 2]) == [1, 1, 2, 2, 3, 3, 3]
    assert sort(items=[5, 5, 5, 5]) == [5, 5, 5, 5]


@pytest.mark.parametrize("sort", SORTS)
def test_negative_numbers(sort):
    assert sort(items=[0, -3, 5, -10, 2, -3]) == [-10, -3, -3, 0, 2, 5]


@pytest.mark.parametrize("sort", SORTS)
def test_floats_and_ints_together(sort):
    assert sort(items=[2, 1.5, -0.5, 1]) == [-0.5, 1, 1.5, 2]


@pytest.mark.parametrize("sort", SORTS)
@pytest.mark.parametrize("seed", range(10))
@pytest.mark.parametrize("size", [2, 17, 100])
def test_matches_reference_on_random_lists(sort, seed, size):
    data = random_list(seed=seed, size=size)

    assert sort(items=data) == sorted(data)


@pytest.mark.parametrize("sort", SORTS)
def test_input_list_is_not_changed(sort):
    data = [3, 1, 2]
    copy = list(data)

    result = sort(items=data)

    assert data == copy
    assert result is not data


@pytest.mark.parametrize("sort", SORTS)
def test_returns_new_list_for_trivial_input(sort):
    empty: list[int] = []
    one = [1]

    assert sort(items=empty) is not empty
    assert sort(items=one) is not one


@pytest.mark.parametrize("sort", SORTS)
def test_tuple_input_gives_list(sort):
    assert sort(items=(3, 1, 2)) == [1, 2, 3]


@pytest.mark.parametrize("sort", SORTS)
@pytest.mark.parametrize("bad", [None, 5, "abc", {3, 1, 2}, iter([1, 2])])
def test_wrong_container_type_raises_type_error(sort, bad):
    with pytest.raises(TypeError):
        sort(items=bad)


@pytest.mark.parametrize("sort", SORTS)
def test_not_comparable_items_raise_type_error(sort):
    with pytest.raises(TypeError):
        sort(items=[1, "a", 2])


@pytest.mark.parametrize("sort", SORTS)
def test_key_function(sort):
    words = ["ccc", "a", "bb", "dddd"]

    assert sort(items=words, key=len) == ["a", "bb", "ccc", "dddd"]
    assert sort(items=[1, -5, 3], key=abs) == [1, 3, -5]


@pytest.mark.parametrize("sort", SORTS)
def test_key_is_called_once_per_item(sort):
    calls = []

    def key(x):
        calls.append(x)
        return x

    sort(items=[4, 2, 3, 1], key=key)

    assert sorted(calls) == [1, 2, 3, 4]


@pytest.mark.parametrize("sort", SORTS)
def test_sort_is_stable(sort):
    items = [(k, i) for i, k in enumerate(random_list(seed=1, size=60, low=0, high=4))]

    result = sort(items=items, key=lambda p: p[0])

    for (k1, i1), (k2, i2) in itertools.pairwise(result):
        assert k1 < k2 or (k1 == k2 and i1 < i2)

