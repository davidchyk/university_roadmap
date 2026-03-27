from __future__ import annotations

import json
from pathlib import Path

def load_json_config(path: str) -> dict:
    raw_data = Path(path).read_text(encoding="utf-8")
    loaded = json.loads(raw_data)

    if not isinstance(loaded, dict):
        raise ValueError("JSON root must be an object")

    return loaded