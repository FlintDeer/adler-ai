
import os
import json
import yaml
from pathlib import Path

class InstructionReference:
    def __init__(self, root=None):
        # Default root path points to one level above this script's directory
        self.root_path = Path(root) if root else Path(__file__).resolve().parents[1]
        self.source_dirs = ["identities", "logs", "memory", "modes"]
        self.output_file = self.root_path / "core" / "instruction_manifest.json"

    def build_manifest(self):
        manifest = {}

        for folder in self.source_dirs:
            dir_path = self.root_path / folder
            category_data = {}

            if not dir_path.exists():
                continue

            for file in dir_path.rglob("*"):
                if file.is_file():
                    if file.suffix in [".md", ".txt"]:
                        with open(file, "r", encoding="utf-8") as f:
                            category_data[file.name] = f.read()
                    elif file.suffix == ".json":
                        with open(file, "r", encoding="utf-8") as f:
                            category_data[file.name] = json.load(f)
                    elif file.suffix in [".yaml", ".yml"]:
                        with open(file, "r", encoding="utf-8") as f:
                            category_data[file.name] = yaml.safe_load(f)

            manifest[folder] = category_data

        # Save to instruction_manifest.json
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return manifest

# Example usage
if __name__ == "__main__":
    ref = InstructionReference()
    instruction_state = ref.build_manifest()
    print(ref.root_path)
