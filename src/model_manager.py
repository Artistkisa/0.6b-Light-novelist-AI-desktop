"""Handle model availability - checks for GGUF file."""
from pathlib import Path

from .config import config


# Default search paths for the GGUF model (relative to working directory)
_DEFAULT_GGUF_PATHS = [
    "T1.gguf",
    "./T1.gguf",
    "models/T1.gguf",
]


def ensure_model() -> str:
    """
    Ensures the GGUF model is available locally.
    Returns the absolute path to the GGUF file.
    """
    # Priority 1: Configured local path
    configured = config.get("model.local_path", "")
    if configured:
        p = Path(configured)
        if p.is_file() and p.suffix == ".gguf":
            print(f"[Model] Using configured GGUF: {p}")
            return str(p.absolute())
        # If it's a directory, look for a .gguf inside
        if p.is_dir():
            ggufs = list(p.glob("*.gguf"))
            if ggufs:
                print(f"[Model] Using GGUF from dir: {ggufs[0]}")
                return str(ggufs[0].absolute())

    # Priority 2: Default search paths
    for rel in _DEFAULT_GGUF_PATHS:
        p = Path(rel)
        if p.is_file():
            print(f"[Model] Using built-in GGUF: {p}")
            return str(p.absolute())

    raise FileNotFoundError(
        "GGUF model not found. Options:\n"
        "1. Place T1.gguf in the app root directory\n"
        "2. Set model.local_path in config/default.yaml"
    )
