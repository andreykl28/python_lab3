import sys

from src import main


def test_main_delegates(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog", "--generator", "rand_int", "--size", "3", "--algos", "quick"])
    main.main()
    output = capsys.readouterr().out
    assert "Данные" in output
