import time
from typing import Callable


def timeit_once(func: Callable, *args, **kwargs) -> float:
    start = time.perf_counter()
    func(*args, **kwargs)
    return time.perf_counter() - start


def benchmark_sorts(arrays: dict[str, list], algos: dict[str, Callable[[list], list]]) -> dict[str, dict[str, float]]:
    results: dict[str, dict[str, float]] = {}
    for arr_name, arr_values in arrays.items():
        results[arr_name] = {}
        for algo_name, algo_func in algos.items():
            results[arr_name][algo_name] = timeit_once(algo_func, arr_values)
    return results
