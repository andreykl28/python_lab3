import pytest

from src.functions import fibo, fibo_recursive, factorial, factorial_recursive


@pytest.mark.parametrize("func", [factorial, factorial_recursive])
def test_factorial_basic(func):
    assert func(0) == 1
    assert func(1) == 1
    assert func(5) == 120


@pytest.mark.parametrize("func", [factorial, factorial_recursive])
def test_factorial_negative(func):
    with pytest.raises(ValueError):
        func(-1)


@pytest.mark.parametrize("func", [fibo, fibo_recursive])
def test_fibo_basic(func):
    assert func(0) == 0
    assert func(1) == 1
    assert func(2) == 1
    assert func(7) == 13


@pytest.mark.parametrize("func", [fibo, fibo_recursive])
def test_fibo_negative(func):
    with pytest.raises(ValueError):
        func(-3)
