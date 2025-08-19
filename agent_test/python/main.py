"""Simple entry point demonstrating HAL9000."""

from .hal9000 import Hal9000


def main() -> None:
    hal = Hal9000()
    response = hal.process_input("Hello, HAL")
    hal.speak(response)


if __name__ == "__main__":
    main()
