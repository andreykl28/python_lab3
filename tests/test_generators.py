import pytest

from src import generators


def test_rand_int_array_distinct_and_seed():
    arr = generators.rand_int_array(5, 1, 10, distinct=True, seed=42)
    assert len(arr) == 5
    assert len(set(arr)) == 5
    assert arr == generators.rand_int_array(5, 1, 10, distinct=True, seed=42)


def test_rand_int_array_plain_branch():
    arr1 = generators.rand_int_array(3, 0, 1, distinct=False, seed=7)
    arr2 = generators.rand_int_array(3, 0, 1, distinct=False, seed=7)
    assert arr1 == arr2


def test_rand_int_array_distinct_error():
    with pytest.raises(ValueError):
        generators.rand_int_array(5, 0, 2, distinct=True)


def test_nearly_sorted_swaps():
    arr = generators.nearly_sorted(5, swaps=2, seed=1)
    assert sorted(arr) == list(range(5))
    assert arr != list(range(5))


def test_many_duplicates_count():
    arr = generators.many_duplicates(10, k_unique=3, seed=2)
    assert len(arr) == 10
    assert max(arr) < 3


def test_reverse_sorted():
    assert generators.reverse_sorted(4) == [4, 3, 2, 1]


def test_rand_float_array_seed():
    arr1 = generators.rand_float_array(3, 0.0, 1.0, seed=5)
    arr2 = generators.rand_float_array(3, 0.0, 1.0, seed=5)
    assert arr1 == arr2
    assert all(0.0 <= x <= 1.0 for x in arr1)
