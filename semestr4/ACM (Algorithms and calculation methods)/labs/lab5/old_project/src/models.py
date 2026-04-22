from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PageConfig:
    page_id: str
    nav_title: str
    title: str
    subtitle: str


@dataclass(frozen=True)
class RootInterval:
    left: float
    right: float

    @property
    def width(self) -> float:
        return abs(self.right - self.left)

    def as_text(self) -> str:
        if self.width == 0:
            return f"x = {self.left:.10f}"
        return f"[{self.left:.10f}; {self.right:.10f}]"


@dataclass(frozen=True)
class IterationRow:
    iteration: int
    left: float
    right: float
    midpoint: float
    f_left: float
    f_midpoint: float
    interval_length: float
    estimated_error: float


@dataclass(frozen=True)
class RootResult:
    interval: RootInterval
    root: float
    function_value: float
    iterations: int
    estimated_error: float
    history: list[IterationRow] = field(default_factory=list)


@dataclass(frozen=True)
class ErrorRow:
    index: int
    interval: RootInterval
    root: float
    function_value: float
    estimated_error: float
    iterations: int
