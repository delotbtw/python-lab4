import random
from collections.abc import Sequence

from algopack.aliases import KeyFunc
from algopack.consts import DEFAULT_SEED
from algopack.errors import InvalidInputError
from algopack.sorting import compute_keys, copy_input


def quickselect[T](
    items: Sequence[T],
    k: int,
    key: KeyFunc | None = None,
    seed: int = DEFAULT_SEED,
) -> T:
    """K-th smallest item, k from 0. Average O(n)"""
    data = copy_input(items=items)
    if isinstance(k, bool) or not isinstance(k, int) or not 0 <= k < len(data):
        raise InvalidInputError(message=f"k must be int in [0, {len(data)}): {k!r}")
    rng = random.Random(seed)
    pairs = list(zip(compute_keys(data=data, key=key), data, strict=True))
    while True:
        pivot = pairs[rng.randrange(len(pairs))][0]
        less = [p for p in pairs if p[0] < pivot]
        equal = [p for p in pairs if not (p[0] < pivot or pivot < p[0])]
        if k < len(less):
            pairs = less
        elif k < len(less) + len(equal):
            return equal[0][1]
        else:
            k -= len(less) + len(equal)
            pairs = [p for p in pairs if pivot < p[0]]
