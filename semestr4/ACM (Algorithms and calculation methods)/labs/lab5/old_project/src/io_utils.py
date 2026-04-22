from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json_config(path: str) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("JSON-конфігурація має бути об'єктом.")

    return data


def save_text_report(path: str, report: str) -> None:
    Path(path).write_text(report, encoding="utf-8")
