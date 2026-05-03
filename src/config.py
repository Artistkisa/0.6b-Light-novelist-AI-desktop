"""Configuration management for Novelist Desktop."""
import os
import yaml
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG = {
    "model": {
        "local_path": "./T1",
        "n_ctx": 4096,
        "n_threads": None,
        "n_batch": 512,
        "temperature": 0.8,
        "top_p": 0.9,
        "repeat_penalty": 1.15,
        "max_tokens": 1024,
    },
    "ui": {
        "title": "超轻量轻小说写手 - 仅0.6B写出14B效果",
        "theme_color": "#667eea",
    },
    "system_prompt": "",
}


class Config:
    def __init__(self, config_path: str = "./config/default.yaml"):
        self.config_path = Path(config_path)
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                user_cfg = yaml.safe_load(f) or {}
            merged = {}
            for section, defaults in DEFAULT_CONFIG.items():
                user_section = user_cfg.get(section, {})
                if isinstance(defaults, dict):
                    merged[section] = {**defaults, **user_section}
                else:
                    merged[section] = user_section if user_section else defaults
            return merged
        return DEFAULT_CONFIG.copy()

    def get(self, key: str, default=None):
        keys = key.split(".")
        val = self._data
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val


config = Config()
