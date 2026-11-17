import random


def random_list(seed: int, size: int, low: int = -50, high: int = 50) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(low, high) for _ in range(size)]
