from algopack.consts import MAX_RECURSIVE_N
from algopack.errors import InvalidInputError


def _check_n(n: object) -> int:
    """Check that n is non negative int"""
    if isinstance(n, bool) or not isinstance(n, int):
        raise InvalidInputError(message=f"n must be int: {n!r}")
    if n < 0:
        raise InvalidInputError(message=f"n must be non negative: {n}")
    return n


def fib_iterative(n: int) -> int:
    """Fibonacci number, F(0)=0, F(1)=1. O(n) time, O(1) memory"""
    n = _check_n(n=n)
    prev, curr = 0, 1
    for _ in range(n):
        prev, curr = curr, prev + curr
    return prev


def _fib_step(n: int, prev: int, curr: int) -> int:
    """Base case n == 0 gives F(0), prev and curr are F(k) and F(k+1)"""
    if n == 0:
        return prev
    return _fib_step(n=n - 1, prev=curr, curr=prev + curr)


def fib_recursive(n: int) -> int:
    """Fibonacci number, F(0)=0, F(1)=1. O(n) time, O(n) stack"""
    n = _check_n(n=n)
    if n > MAX_RECURSIVE_N:
        raise InvalidInputError(
            message=f"n too big for recursion: {n} > {MAX_RECURSIVE_N}"
        )
    return _fib_step(n=n, prev=0, curr=1)
