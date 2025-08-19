"""HAL9000 core interface."""

class Hal9000:
    def __init__(self):
        # Initialization logic placeholder
        pass

    def process_input(self, text: str) -> str:
        """Process incoming text and return a response."""
        return f"Processing: {text}"

    def speak(self, message: str) -> None:
        """Output a message."""
        print(f"HAL9000: {message}")
