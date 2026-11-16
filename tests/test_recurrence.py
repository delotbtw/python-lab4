import pytest

from algopack.consts import MAX_RECURSIVE_N
from algopack.errors import AlgoError, InvalidInputError
from algopack.recurrence import fib_iterative, fib_recursive

FIRST = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
FUNCS = [fib_iterative, fib_recursive]


@pytest.mark.parametrize("func", FUNCS)
def test_first_numbers(func):
    assert [func(n=n) for n in range(len(FIRST))] == FIRST


def test_variants_match_on_range():
    for n in range(200):
        assert fib_iterative(n=n) == fib_recursive(n=n)


def test_iterative_handles_big_n():
    assert fib_iterative(n=1000) % 10 == 5


@pytest.mark.parametrize("func", FUNCS)
@pytest.mark.parametrize("bad", [-1, 1.5, "5", None, True])
def test_invalid_input(func, bad):
    with pytest.raises(InvalidInputError):
        func(n=bad)


def test_recursive_limit_is_checked_before_recursion():
    with pytest.raises(InvalidInputError):
        fib_recursive(n=MAX_RECURSIVE_N + 1)


def test_recursive_works_on_limit():
    assert fib_recursive(n=MAX_RECURSIVE_N) == fib_iterative(n=MAX_RECURSIVE_N)


def test_error_is_package_error():
    with pytest.raises(AlgoError):
        fib_recursive(n=-5)
