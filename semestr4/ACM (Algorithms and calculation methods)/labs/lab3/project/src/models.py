from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PageConfig:
    page_id: str
    nav_title: str
    title: str
    subtitle: str


@dataclass(frozen=True)
class ErrorRow:
    degree: int
    approximation: float
    estimate: float | None
    actual_error: float