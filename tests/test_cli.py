import sys
from types import SimpleNamespace

from src import cli


def test_generate_data_variants():
    args = SimpleNamespace(
        generator="rand_int",
        size=3,
        lo=0,
        hi=5,
        distinct=False,
        swaps=1,
        k_unique=2,
        seed=1,
        buckets=None,
        base=10,
        algos=["quick"],
    )
    data = cli.generate_data(args)
    assert len(data) == 3

    args.generator = "nearly_sorted"
    data2 = cli.generate_data(args)
    assert sorted(data2) == list(range(3))

    args.generator = "rand_float"
    data3 = cli.generate_data(args)
    assert len(data3) == 3

    args.generator = "many_duplicates"
    data4 = cli.generate_data(args)
    assert len(data4) == 3

    args.generator = "reverse_sorted"
    data5 = cli.generate_data(args)
    assert data5 == [3, 2, 1]


def test_select_algos_filters(monkeypatch):
    args = SimpleNamespace(
        base=10,
        buckets=None,
        algos=["bubble", "quick", "counting", "radix", "bucket", "heap"],
    )
    sample_ints = [1, 2, 3]
    selected = cli.select_algos(args, sample_ints)
    assert set(selected.keys()) == {"bubble", "quick", "counting", "radix", "bucket", "heap"}

    sample_floats = [0.1, 0.2]
    selected = cli.select_algos(args, sample_floats)
    # counting/radix должны отвалиться
    assert "counting" not in selected and "radix" not in selected
    assert "bucket" in selected


def test_print_results(capsys):
    cli.print_results({"arr": {"quick": 0.001, "bubble": 0.01}})
    captured = capsys.readouterr().out
    assert "arr" in captured
    assert "quick" in captured
    assert "bubble" in captured


def test_main_invokes_cli(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog", "--generator", "rand_int", "--size", "3", "--algos", "quick"])
    cli.main()
    assert "Данные" in capsys.readouterr().out
