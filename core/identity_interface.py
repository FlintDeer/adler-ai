import yaml
import os

IDENTITY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "identities", "adler.yaml"))

class IdentityManifest:
    def __init__(self, path=IDENTITY_PATH):
        self.path = path
        self.data = self._load()

    def _load(self):
        with open(self.path, 'r') as file:
            return yaml.safe_load(file)
    
    def get(self, key_path):
        keys = key_path.split('.');
        ref = self.data
        for key in keys:
            ref = ref.get(key, {})
        return ref

    def set(self, key_path, value):
        keys = key_path.split('.')
        ref = self.data
        for key in keys[:-1]:
            if key not in ref:
                ref[key] = {}
            ref = ref[key]
        ref[keys[-1]] = value
        self._save()
    
    def _save(self):
        with open(self.path, 'w') as file:
            yaml.dump(self.data, file, sort_keys=False)

if __name__ == "__main__":
    identity = IdentityManifest()

    identity.set("behavior.emotion_filter", "none")

    print(identity.get("behavior"))