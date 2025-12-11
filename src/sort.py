from functools import cmp_to_key
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def compare(left: T, right: T, key: Callable[[T], Any] | None, cmp: Callable[[T, T], int] | None) -> int:
    """Сравнение двух элементов с учетом key или cmp."""
    if cmp is not None:
        return cmp(left, right)
    if key is not None:
        l_val, r_val = key(left), key(right)
    else:
        l_val, r_val = left, right
    return (l_val > r_val) - (l_val < r_val)


def bubble_sort(a: list[T], key: Callable[[T], Any] | None = None, cmp: Callable[[T, T], int] | None = None) -> list[T]:
    """Пузырьковая сортировка (стабильная)."""
    result = a.copy()
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if compare(result[j], result[j + 1], key, cmp) > 0:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result


def quick_sort(a: list[T], key: Callable[[T], Any] | None = None, cmp: Callable[[T, T], int] | None = None) -> list[T]:
    """Быстрая сортировка с разбиением на три части и склейкой."""
    if len(a) <= 1:
        return a.copy()
    pivot = a[len(a) // 2]
    less: list[T] = []
    equal: list[T] = []
    greater: list[T] = []
    for item in a:
        cmp_result = compare(item, pivot, key, cmp)
        if cmp_result < 0:
            less.append(item)
        elif cmp_result > 0:
            greater.append(item)
        else:
            equal.append(item)
    return quick_sort(less, key, cmp) + equal + quick_sort(greater, key, cmp)


def counting_sort(
    a: list[T], key: Callable[[T], int] | None = None, cmp: Callable[[T, T], int] | None = None
) -> list[T]:
    """Подсчет для целых значений (стабильная). При cmp делаем простой стабильный проход вставками."""
    if not a:
        return []
    if cmp is not None:
        result = a.copy()
        for i in range(1, len(result)):
            current = result[i]
            j = i - 1
            while j >= 0 and compare(result[j], current, key, cmp) > 0:
                result[j + 1] = result[j]
                j -= 1
            result[j + 1] = current
        return result

    values = [key(x) if key else x for x in a]
    if not all(isinstance(value, int) for value in values):
        raise TypeError("counting_sort поддерживает только целые ключи")
    min_val, max_val = min(values), max(values)
    size = max_val - min_val + 1
    counts = [0] * size
    for value in values:
        counts[value - min_val] += 1
    for i in range(1, size):
        counts[i] += counts[i - 1]
    output: list[T] = [a[0]] * len(a)
    for item, v in zip(reversed(a), reversed(values)):
        counts[v - min_val] -= 1
        output[counts[v - min_val]] = item
    return output


def radix_sort(
    a: list[T], base: int = 10, key: Callable[[T], Any] | None = None, cmp: Callable[[T, T], int] | None = None
) -> list[T]:
    """
    Радикс для неотрицательных целых ключей. Сохраняет порядок равных (стабильная).
    cmp не поддерживается, key должен возвращать целое.
    """
    if not a:
        return []
    if cmp is not None:
        raise TypeError("radix_sort не поддерживает cmp")
    values = [key(x) if key else x for x in a]
    if not all(isinstance(value, int) and value >= 0 for value in values):
        raise ValueError("radix_sort поддерживает только неотрицательные целые ключи")

    paired = list(zip(values, a))
    max_val = max(values)
    exp = 1
    result = paired
    while max_val // exp > 0:
        buckets: list[list[tuple[int, T]]] = [[] for _ in range(base)]
        for key_val, item in result:
            bucket_idx = (key_val // exp) % base
            buckets[bucket_idx].append((key_val, item))
        result = [kv for bucket in buckets for kv in bucket]
        exp *= base
    return [item for _, item in result]


def bucket_sort(
    a: list[T],
    buckets: int | None = None,
    key: Callable[[T], Any] | None = None,
    cmp: Callable[[T, T], int] | None = None,
) -> list[T]:
    """Бакет-сорт. По умолчанию ожидает числа, при необходимости нормализует в [0, 1). Поддерживает key/cmp внутри бакета."""
    if not a:
        return []

    key_func = key or (lambda x: x)
    values = [key_func(x) for x in a]
    if not all(isinstance(value, (int, float)) for value in values):
        raise TypeError("bucket_sort поддерживает только числовые значения или key")

    min_val, max_val = min(values), max(values)
    span = max_val - min_val or 1.0
    size = buckets or len(a)
    bins: list[list[T]] = [[] for _ in range(size)]

    for item, val in zip(a, values):
        normalized = (val - min_val) / span
        idx = min(size - 1, int(normalized * size))
        bins[idx].append(item)

    result: list[T] = []
    for bucket in bins:
        for i in range(1, len(bucket)):
            current = bucket[i]
            j = i - 1
            while j >= 0 and compare(bucket[j], current, key_func, cmp) > 0:
                bucket[j + 1] = bucket[j]
                j -= 1
            bucket[j + 1] = current
        result.extend(bucket)
    return result


def heap_sort(a: list[T], key: Callable[[T], Any] | None = None, cmp: Callable[[T, T], int] | None = None) -> list[T]:
    """Сортировка кучей. Работает с key/cmp, возвращает новый список."""
    result = []
    cmp_key = cmp_to_key(cmp) if cmp else None

    def make_key(item: T) -> Any:
        if cmp_key:
            return cmp_key(item)
        return key(item) if key else item

    heap = [(make_key(item), idx, item) for idx, item in enumerate(a)]

    def sift_down(arr: list[tuple[Any, int, T]], start: int, end: int) -> None:
        root = start
        while True:
            child = 2 * root + 1
            if child > end:
                break
            if child + 1 <= end and arr[child + 1][0] < arr[child][0]:
                child += 1
            if arr[root][0] <= arr[child][0]:
                break
            arr[root], arr[child] = arr[child], arr[root]
            root = child

    n = len(heap)
    for start in range((n - 2) // 2, -1, -1):
        sift_down(heap, start, n - 1)
    for end in range(n - 1, -1, -1):
        heap[0], heap[end] = heap[end], heap[0]
        result.append(heap[end][2])
        sift_down(heap, 0, end - 1)
    return result
