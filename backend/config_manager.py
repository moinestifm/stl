import yaml
import os

class ConfigManager:
    def __init__(self, config_dir="configs"):
        self.config_dir = config_dir
        os.makedirs(config_dir, exist_ok=True)

    def load_config(self, filename):
        path = os.path.join(self.config_dir, filename)
        with open(path) as f:
            return yaml.safe_load(f)

    def save_config(self, filename, data):
        path = os.path.join(self.config_dir, filename)
        with open(path, "w") as f:
            yaml.dump(data, f)
