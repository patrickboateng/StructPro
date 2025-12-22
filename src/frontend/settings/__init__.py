import json
from pathlib import Path

from collections import UserDict
from types import SimpleNamespace

settings_path = Path(__file__).resolve().parent / "settings.json"
settings = None


class Settings(UserDict):

    def __getitem__(self, key):
        return SimpleNamespace(super().__getitem__(key))

    def __getattr__(self, name):
        return super().__getitem__(name)


def load_settings() -> Settings:
    global settings
    if settings is None:
        with open(settings_path, "r") as f:
            settings = Settings(json.load(f))

    return settings


def save_settings() -> None:
    global settings
    with open(settings_path, "w") as f:
        json.dump(settings.data, f)
