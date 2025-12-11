import pytest

from src import sort


def test_bubble_sort_with_key():
    data = ["ccc", "b", "aa"]
    res = sort.bubble_sort(data, key=len)
    assert res == ["b", "aa", "ccc"]
    assert data == ["ccc", "b", "aa"]  # не меняет оригинал


def test_quick_sort_with_cmp():
    data = [3, 1, 2]
    res = sort.quick_sort(data, cmp=lambda a, b: (a % 2) - (b % 2) or (a - b))
    assert res == [2, 1, 3]  # чётные сначала, внутри по возрастанию


def test_counting_sort_int_keys():
    data = [5, 3, 5, 4]
    assert sort.counting_sort(data) == [3, 4, 5, 5]


def test_counting_sort_with_cmp_fallback():
    data = ["bb", "a", "ccc"]
    res = sort.counting_sort(data, cmp=lambda a, b: len(a) - len(b))
    assert res == ["a", "bb", "ccc"]


def test_counting_sort_type_error():
    with pytest.raises(TypeError):
        sort.counting_sort([1.2, 3])

def test_counting_sort_empty():
    assert sort.counting_sort([]) == []


def test_radix_sort_plain():
    data = [170, 45, 75, 90, 802, 24, 2, 66]
    assert sort.radix_sort(data) == sorted(data)


def test_radix_sort_with_key_and_non_negative():
    data = [{"n": 3}, {"n": 1}, {"n": 2}]
    res = sort.radix_sort(data, key=lambda x: x["n"])
    assert res == [{"n": 1}, {"n": 2}, {"n": 3}]


def test_radix_sort_reject_cmp_and_negative():
    with pytest.raises(TypeError):
        sort.radix_sort([1, 2], cmp=lambda a, b: a - b)
    with pytest.raises(ValueError):
        sort.radix_sort([-1, 2])

def test_radix_sort_empty():
    assert sort.radix_sort([]) == []


def test_bucket_sort_normalizes_numbers():
    data = [10, 5, 15]
    res = sort.bucket_sort(data)
    assert res == [5, 10, 15]


def test_bucket_sort_with_key_and_cmp():
    data = [{"x": 0.1}, {"x": 0.05}, {"x": 0.2}]
    res = sort.bucket_sort(data, key=lambda v: v["x"], cmp=lambda a, b: (a["x"] > b["x"]) - (a["x"] < b["x"]))
    assert res == [{"x": 0.05}, {"x": 0.1}, {"x": 0.2}]


def test_bucket_sort_type_error():
    with pytest.raises(TypeError):
        sort.bucket_sort(["a", "b"])

def test_bucket_sort_empty():
    assert sort.bucket_sort([]) == []


def test_heap_sort_with_key_and_cmp():
    data = ["bbb", "a", "cc"]
    res = sort.heap_sort(data, key=len, cmp=None)
    assert res == ["a", "cc", "bbb"]


def test_heap_sort_stability_on_equal_keys():
    data = [("a", 1), ("b", 1), ("c", 0)]
    res = sort.heap_sort(data, key=lambda x: x[1])
    assert res == [("c", 0), ("a", 1), ("b", 1)]
