import pytest

from algopack.errors import AlgoError, EmptyStructureError, InvalidInputError
from algopack.priority_queue import PriorityQueue
from tests.helpers import random_list


def test_new_queue_is_empty():
    queue = PriorityQueue()

    assert len(queue) == 0
    assert not queue


def test_pop_on_empty_raises():
    with pytest.raises(EmptyStructureError):
        PriorityQueue().pop()


def test_peek_on_empty_raises():
    with pytest.raises(EmptyStructureError):
        PriorityQueue().peek()


def test_empty_error_is_package_error():
    with pytest.raises(AlgoError):
        PriorityQueue().pop()


def test_error_after_queue_becomes_empty_again():
    queue = PriorityQueue()
    queue.push(item="a", priority=1)
    queue.pop()

    with pytest.raises(EmptyStructureError):
        queue.pop()


def test_push_changes_len_and_bool():
    queue = PriorityQueue()
    queue.push(item="a", priority=2)
    queue.push(item="b", priority=1)

    assert len(queue) == 2
    assert queue


def test_peek_returns_smallest_without_removing():
    queue = PriorityQueue()
    queue.push(item="low", priority=5)
    queue.push(item="high", priority=1)

    assert queue.peek() == "high"
    assert len(queue) == 2


def test_pop_order_by_priority():
    queue = PriorityQueue()
    for item, priority in [("c", 3), ("a", 1), ("d", 4), ("b", 2)]:
        queue.push(item=item, priority=priority)

    assert [queue.pop() for _ in range(4)] == ["a", "b", "c", "d"]


def test_equal_priorities_keep_insert_order():
    queue = PriorityQueue()
    for item in "abcde":
        queue.push(item=item, priority=1)

    assert [queue.pop() for _ in range(5)] == list("abcde")


def test_negative_and_float_priorities():
    queue = PriorityQueue()
    queue.push(item="x", priority=-1.5)
    queue.push(item="y", priority=-10)
    queue.push(item="z", priority=0)

    assert [queue.pop() for _ in range(3)] == ["y", "x", "z"]


def test_items_do_not_need_to_be_comparable():
    queue = PriorityQueue()
    queue.push(item={"a": 1}, priority=1)
    queue.push(item={"b": 2}, priority=1)

    assert queue.pop() == {"a": 1}


@pytest.mark.parametrize("bad", ["1", None, True, float("nan")])
def test_bad_priority_raises(bad):
    with pytest.raises(InvalidInputError):
        PriorityQueue().push(item="x", priority=bad)


def test_heap_invariant_holds_after_every_operation():
    queue = PriorityQueue()
    for i, priority in enumerate(random_list(seed=7, size=100)):
        queue.push(item=i, priority=priority)
        assert queue.is_valid_heap()
    while queue:
        queue.pop()
        assert queue.is_valid_heap()


def test_pop_order_matches_sorted_priorities():
    priorities = random_list(seed=5, size=200)
    queue = PriorityQueue()
    for i, priority in enumerate(priorities):
        queue.push(item=priority, priority=priority)
        assert len(queue) == i + 1

    assert [queue.pop() for _ in priorities] == sorted(priorities)
