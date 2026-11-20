import pytest

from algopack.select import quickselect
from tests.helpers import random_list


@pytest.mark.parametrize("seed", range(10))
def test_matches_sorted_for_every_k(seed):
    data = random_list(seed=seed, size=40)
    expected = sorted(data)

    assert [quickselect(items=data, k=k) for k in range(len(data))] == expected


def test_single_item():
    assert quickselect(items=[5], k=0) == 5


def test_all_equal_items():
    assert quickselect(items=[2, 2, 2, 2], k=3) == 2


def test_negative_numbers():
    assert quickselect(items=[3, -1, -7, 0], k=0) == -7


def test_input_is_not_changed():
    data = [5, 3, 1, 4]

    quickselect(items=data, k=2)

    assert data == [5, 3, 1, 4]


def test_key_function():
    assert quickselect(items=["ccc", "a", "bb"], k=1, key=len) == "bb"


def test_same_seed_same_result_for_equal_keys():
    items = [(1, "a"), (1, "b"), (1, "c")]

    first = quickselect(items=items, k=1, key=lambda p: p[0], seed=3)

    assert first == quickselect(items=items, k=1, key=lambda p: p[0], seed=3)


def test_wrong_container_type_raises_type_error():
    with pytest.raises(TypeError):
        quickselect(items=None, k=0)
