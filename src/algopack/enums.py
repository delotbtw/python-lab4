from enum import Enum


class InputKind(Enum):
    RANDOM = "random"
    SORTED = "sorted"
    REVERSED = "reversed"
    NEARLY_SORTED = "nearly_sorted"
    MANY_DUPLICATES = "many_duplicates"


class Complexity(Enum):
    QUADRATIC = "O(n^2)"
    N_LOG_N = "O(n log n)"
