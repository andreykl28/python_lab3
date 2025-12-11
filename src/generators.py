import random


def rand_int_array(n: int, lo: int, hi: int, *, distinct: bool = False, seed: int | None = None) -> list[int]:
    rng = random.Random(seed) if seed is not None else random
    if distinct:
        if hi - lo + 1 < n:
            raise ValueError("Диапазон слишком мал для distinct")
        return rng.sample(range(lo, hi + 1), n)
    return [rng.randint(lo, hi) for _ in range(n)]


def nearly_sorted(n: int, swaps: int, *, seed: int | None = None) -> list[int]:
    arr = list(range(n))
    rng = random.Random(seed) if seed is not None else random
    for _ in range(swaps):
        i, j = rng.randint(0, n - 1), rng.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def many_duplicates(n: int, k_unique: int = 5, *, seed: int | None = None) -> list[int]:
    rng = random.Random(seed) if seed is not None else random
    return [rng.randint(0, k_unique - 1) for _ in range(n)]


def reverse_sorted(n: int) -> list[int]:
    return list(range(n, 0, -1))


def rand_float_array(n: int, lo: float = 0.0, hi: float = 1.0, *, seed: int | None = None) -> list[float]:
    rng = random.Random(seed) if seed is not None else random
    return [rng.uniform(lo, hi) for _ in range(n)]
