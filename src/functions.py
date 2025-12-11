from functools import lru_cache


def factorial(num: int) -> int:
    """Факториал числа через цикл."""
    if num < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    result = 1
    while num > 1:
        result *= num
        num -= 1
    return result

@lru_cache(maxsize=None)
def factorial_recursive(num: int) -> int:
    """Факториал числа через рекурсию."""
    if num < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    if num <= 1:
        return 1
    return num * factorial_recursive(num - 1)


def fibo(num: int) -> int:
    """Число Фибоначчи по индексу через цикл. Начальные условия: F(0)=0, F(1)=1."""
    if num < 0:
        raise ValueError("Индекс числа Фибоначчи не может быть отрицательным")
    if num == 0:
        return 0
    if num == 1:
        return 1
    prev, curr = 0, 1
    for _ in range(2, num + 1):
        prev, curr = curr, prev + curr
    return curr


@lru_cache(maxsize=None)
def fibo_recursive(num: int) -> int:
    """Число Фибоначчи по индексу через рекурсию. Начальные условия: F(0)=0, F(1)=1."""
    if num < 0:
        raise ValueError("Индекс числа Фибоначчи не может быть отрицательным")
    if num == 0:
        return 0
    if num == 1:
        return 1
    return fibo_recursive(num - 1) + fibo_recursive(num - 2)


