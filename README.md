# Лабораторная работа 3 (вариант: Medium)

Алгоритмический мини‑пакет: функции факториала и Фибоначчи, набор сортировок, стек/очередь, генераторы тестовых данных и CLI для бенчмарков. 

Цель — сделать универсальные реализации с поддержкой `key`/`cmp`, проверкой входных данных и набором тестов.

## Состав
- Последовательности: `factorial`, `factorial_recursive`, `fibo`, `fibo_recursive` (проверка на некорректные входы, кеш для рекурсивных).
- Сортировки: `bubble_sort`, `quick_sort`, `counting_sort`, `radix_sort`, `bucket_sort`, `heap_sort` с поддержкой `key`/`cmp` там, где это уместно (counting/radix валидируют целочисленные ключи, bucket нормализует числовые).
- Структуры данных: `Stack` с `min()` за O(1), `Queue` на двух стеках; выдают `IndexError` на некорректных операциях.
- Генераторы: `rand_int_array`, `nearly_sorted`, `many_duplicates`, `reverse_sorted`, `rand_float_array`.
- Бенчмарки: `timeit_once`, `benchmark_sorts` и CLI для прогонов.

## Структура
- `src/functions.py` — факториал и Фибоначчи.
- `src/sort.py` — сортировки с `key`/`cmp` и валидацией входов.
- `src/data_structures.py` — стек/очередь.
- `src/generators.py` — генераторы массивов.
- `src/benchmarks.py` — таймеры для сортировок.
- `src/cli.py` — интерфейс командной строки (генерация данных, запуск сортировок, вывод времени).
- `src/main.py` — точка входа, делегирует на CLI.
- `tests/` — pytest‑тесты для всех компонентов.

## Установка и запуск
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # файл содержит dev-зависимости для тестов
```

Запуск CLI (генерация и бенчмарк):
```bash
python -m src.main --generator rand_int --size 1000 --algos quick heap
python -m src.main --help
```

Пример прямого использования в коде:
```python
from src import sort
data = sort.quick_sort([3, 1, 2])
```

## Тесты и покрытие
```bash
python -m pytest
python -m pytest --cov=src --cov-report=term-missing
```
Текущее покрытие ~94% (pytest‑тесты в каталоге `tests`).

## Особенности
- `counting_sort`/`radix_sort` принимают только целочисленные ключи (radix — неотрицательные); при неверных входах поднимают исключения.
- `bucket_sort` работает с числовыми данными, при необходимости нормализует их в [0,1) и сортирует внутри бакетов вставками.
- CLI автоматически пропускает неподходящие алгоритмы для выбранных данных и выводит времена выполнения.
