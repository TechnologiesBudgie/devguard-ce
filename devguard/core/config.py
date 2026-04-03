import yaml
from pathlib import Path
from typing import List

class Config:
    def __init__(self, config_path: str = ".devguard.yml"):
        self.config_path = Path(config_path)
        self.ai_enabled = False
        self.ignore_dirs = [".git", "node_modules", "venv"]
        self.ignore_extensions = [".pyc", ".png", ".jpg", ".bin"]
        self.load()

    def load(self):
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                data = yaml.safe_load(f) or {}
                self.ai_enabled = data.get("ai_enabled", self.ai_enabled)
                self.ignore_dirs = data.get("ignore_dirs", self.ignore_dirs)
                self.ignore_extensions = data.get("ignore_extensions", self.ignore_extensions)

    def save(self):
        with open(self.config_path, "w") as f:
            yaml.safe_dump({
                "ai_enabled": self.ai_enabled,
                "ignore_dirs": self.ignore_dirs,
                "ignore_extensions": self.ignore_extensions
            }, f)
