from src.cli import main as cli_main


def main() -> None:
    """Точка входа: делегирует запуск CLI сортировок/бенчмарков."""
    cli_main()


if __name__ == "__main__":  # pragma: no cover
    main()
