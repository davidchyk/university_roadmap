from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.models import MatrixProblem, NumberMatrix, NumberVector


def load_system_config(path: str) -> MatrixProblem:
    with Path(path).open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("JSON-файл має містити об'єкт.")

    matrix_source = _first_present(data, "matrix", "coefficients", "a")
    vector_source = _first_present(data, "vector", "rhs", "b")
    name = str(data.get("name", "Система з JSON"))

    matrix = _parse_matrix(matrix_source)
    vector = _parse_vector(vector_source)
    return MatrixProblem(name=name, matrix=matrix, vector=vector)


def save_text_report(path: str, report: str) -> None:
    Path(path).write_text(report, encoding="utf-8")


def _first_present(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data:
            return data[key]
    raise ValueError(f"JSON має містити одне з полів: {', '.join(keys)}.")


def _parse_matrix(value: Any) -> NumberMatrix:
    if not isinstance(value, list) or not value:
        raise ValueError("Матриця має бути непорожнім двовимірним масивом.")

    matrix: NumberMatrix = []
    for row in value:
        if not isinstance(row, list) or not row:
            raise ValueError("Кожен рядок матриці має бути непорожнім масивом.")
        matrix.append([_parse_number(item) for item in row])
    return matrix


def _parse_vector(value: Any) -> NumberVector:
    if not isinstance(value, list) or not value:
        raise ValueError("Вектор b має бути непорожнім масивом.")
    return [_parse_number(item) for item in value]


def _parse_number(value: Any) -> float:
    if isinstance(value, bool):
        raise ValueError("Логічні значення не є числами для СЛАР.")
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        normalized = value.strip().replace(",", ".")
        if not normalized:
            raise ValueError("Порожній рядок не можна перетворити на число.")
        return float(normalized)
    raise ValueError(f"Непідтримуване числове значення: {value!r}.")
