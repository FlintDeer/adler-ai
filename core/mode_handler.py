
import os
import json

MODES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modes"))

class ModeHandler:
    def __init__(self, default_mode='neutral'):
        self.active_mode = default_mode
        self.mode_path = os.path.join(MODES_DIR, f"{self.active_mode}.md")

    def set_mode(self, mode_name):
        mode_file = os.path.join(MODES_DIR, f"{mode_name}.md")
        if os.path.exists(mode_file):
            self.active_mode = mode_name
            self.mode_path = mode_file
            return f"Mode switched to '{mode_name}'"
        else:
            return f"Mode '{mode_name}' not found."

    def get_active_mode(self):
        return self.active_mode

    def get_mode_description(self):
        try:
            with open(self.mode_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "Active mode file not found."

# Example usage
if __name__ == "__main__":
    handler = ModeHandler()
    print(handler.set_mode("default"))  # Change mode
    print("--- Mode Description ---")
    print(handler.get_mode_description())
