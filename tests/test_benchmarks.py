from src.benchmarks import benchmark_sorts, timeit_once
from src import sort


def test_timeit_once_returns_positive():
    elapsed = timeit_once(sum, [1, 2, 3])
    assert elapsed >= 0


def test_benchmark_sorts_structure():
    arrays = {"small": [3, 1, 2]}
    algos = {"quick": sort.quick_sort, "bubble": sort.bubble_sort}
    results = benchmark_sorts(arrays, algos)
    assert set(results.keys()) == {"small"}
    assert set(results["small"].keys()) == {"quick", "bubble"}
    assert all(isinstance(v, float) for v in results["small"].values())
