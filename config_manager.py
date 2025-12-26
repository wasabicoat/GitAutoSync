import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_path = Path.home() / ".gitautosync_config.json"
        self.config = self.load_config()

    def load_config(self):
        if not self.config_path.exists():
            return {"monitored_paths": []}
        
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {"monitored_paths": []}

    def save_config(self):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except OSError as e:
            print(f"Error saving config: {e}")

    def get_paths(self):
        return self.config.get("monitored_paths", [])

    def add_path(self, path):
        paths = self.get_paths()
        if path not in paths:
            paths.append(path)
            self.config["monitored_paths"] = paths
            self.save_config()
            return True
        return False

    def remove_path(self, path):
        paths = self.get_paths()
        if path in paths:
            paths.remove(path)
            self.config["monitored_paths"] = paths
            self.save_config()
            return True
        return False
