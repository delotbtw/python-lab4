from collections.abc import Sequence
from typing import Any

from algopack.aliases import KeyFunc


def copy_input[T](items: Sequence[T]) -> list[T]:
    """Return copy of list or tuple, other types are not allowed"""
    if not isinstance(items, list | tuple):
        raise TypeError(f"expected list or tuple, got {type(items).__name__}")
    return list(items)


def compute_keys[T](data: list[T], key: KeyFunc | None) -> list[Any]:
    """Key for each item, key function is called once per item"""
    if key is None:
        return list(data)
    return [key(item) for item in data]


def insertion_sort[T](items: Sequence[T], key: KeyFunc | None = None) -> list[T]:
    """New sorted list, stable. O(n^2), TypeError on bad input"""
    data = copy_input(items=items)
    keys = compute_keys(data=data, key=key)
    for i in range(1, len(data)):
        cur_item, cur_key = data[i], keys[i]
        j = i - 1
        while j >= 0 and cur_key < keys[j]:
            data[j + 1] = data[j]
            keys[j + 1] = keys[j]
            j -= 1
        data[j + 1] = cur_item
        keys[j + 1] = cur_key
    return data
