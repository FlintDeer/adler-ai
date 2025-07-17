import os
import json
import yaml

class InstructionReference:
    def __init__(self):
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.modes_path = os.path.join(self.base_path, "modes")
        self.identities_path = os.path.join(self.base_path, "identities")
        self.memory_path = os.path.join(self.base_path, "memory")
        self.output_path = os.path.join(self.base_path, "instruction_manifest.json")

    def read_file(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def read_yaml(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def read_identity_memory(self, identity_name):
        profile_name = identity_name.replace(".yaml", "")
        profile_memory_dir = os.path.join(self.memory_path, profile_name)
        memory_entries = {}

        if os.path.exists(profile_memory_dir):
            for fname in os.listdir(profile_memory_dir):
                fpath = os.path.join(profile_memory_dir, fname)
                memory_entries[fname] = self.read_file(fpath)

        return memory_entries

    def build_manifest(self, current_mode, current_identity):
        mode_file = os.path.join(self.modes_path, current_mode + ".md")
        identity_file = os.path.join(self.identities_path, current_identity, current_identity + ".json")

        mode_description = self.read_file(mode_file)

        with open(identity_file, 'r') as f:
            # Load the JSON data into a Python dictionary or list
            data = json.load(f)

        manifest = data

        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

        return manifest