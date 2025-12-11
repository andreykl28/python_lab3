import argparse
import sys
from typing import Callable

from src import sort
from src.benchmarks import benchmark_sorts
from src.generators import (
    many_duplicates,
    nearly_sorted,
    rand_float_array,
    rand_int_array,
    reverse_sorted,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Запуск сортировок и бенчмарков.")
    parser.add_argument("--generator", choices=[
        "rand_int",
        "nearly_sorted",
        "many_duplicates",
        "reverse_sorted",
        "rand_float",
    ], default="rand_int", help="Какой набор данных сгенерировать")
    parser.add_argument("--size", type=int, default=1000, help="Размер массива")
    parser.add_argument("--lo", type=float, default=0, help="Нижняя граница для генерации")
    parser.add_argument("--hi", type=float, default=1000, help="Верхняя граница для генерации")
    parser.add_argument("--distinct", action="store_true", help="Уникальные значения для rand_int")
    parser.add_argument("--swaps", type=int, default=10, help="Количество обменов для nearly_sorted")
    parser.add_argument("--k-unique", type=int, default=5, dest="k_unique", help="Различных значений для many_duplicates")
    parser.add_argument("--seed", type=int, default=None, help="Seed для генератора")
    parser.add_argument("--buckets", type=int, default=None, help="Число бакетов для bucket_sort")
    parser.add_argument("--base", type=int, default=10, help="Основание для radix_sort")
    parser.add_argument("--algos", nargs="*", default=[
        "bubble",
        "quick",
        "counting",
        "radix",
        "bucket",
        "heap",
    ], help="Какие алгоритмы запускать (имена через пробел)")
    return parser


def generate_data(args: argparse.Namespace) -> list:
    if args.generator == "rand_int":
        return rand_int_array(args.size, int(args.lo), int(args.hi), distinct=args.distinct, seed=args.seed)
    if args.generator == "nearly_sorted":
        return nearly_sorted(args.size, args.swaps, seed=args.seed)
    if args.generator == "many_duplicates":
        return many_duplicates(args.size, args.k_unique, seed=args.seed)
    if args.generator == "reverse_sorted":
        return reverse_sorted(args.size)
    if args.generator == "rand_float":
        return rand_float_array(args.size, args.lo, args.hi, seed=args.seed)
    raise ValueError("Неизвестный генератор")


def select_algos(args: argparse.Namespace, sample: list) -> dict[str, Callable[[list], list]]:
    available: dict[str, Callable[[list], list]] = {
        "bubble": sort.bubble_sort,
        "quick": sort.quick_sort,
        "counting": sort.counting_sort,
        "radix": lambda arr: sort.radix_sort(arr, base=args.base),
        "bucket": lambda arr: sort.bucket_sort(arr, buckets=args.buckets),
        "heap": sort.heap_sort,
    }
    chosen = {name for name in args.algos if name in available}
    if not chosen:
        raise ValueError("Не выбрано ни одного алгоритма из доступных")

    is_all_ints = all(isinstance(x, int) for x in sample)
    has_negative = any(isinstance(x, int) and x < 0 for x in sample)
    has_float = any(isinstance(x, float) and not isinstance(x, bool) for x in sample)

    filtered: dict[str, Callable[[list], list]] = {}
    for name in chosen:
        if name == "counting" and not is_all_ints:
            print("[skip] counting_sort: нужны целые ключи", file=sys.stderr)
            continue
        if name == "radix":
            if not is_all_ints or has_negative:
                print("[skip] radix_sort: нужны неотрицательные целые", file=sys.stderr)
                continue
        if name == "bucket":
            # bucket_sort умеет нормализовать числа, но не работает с нечисловыми
            if not is_all_ints and not has_float:
                print("[skip] bucket_sort: нужны числовые данные", file=sys.stderr)
                continue
        filtered[name] = available[name]

    if not filtered:
        raise ValueError("Нет подходящих алгоритмов для выбранных данных")
    return filtered


def print_results(results: dict[str, dict[str, float]]) -> None:
    for arr_name, timings in results.items():
        print(f"\nДанные: {arr_name}")
        for algo_name, elapsed in sorted(timings.items(), key=lambda x: x[1]):
            print(f"  {algo_name:10s} {elapsed:.6f} c")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    data = generate_data(args)
    algos = select_algos(args, data)
    results = benchmark_sorts({args.generator: data}, algos)
    print_results(results)


if __name__ == "__main__":
    main()
