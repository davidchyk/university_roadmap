from __future__ import annotations

from dataclasses import dataclass, field


NumberMatrix = list[list[float]]
NumberVector = list[float]


@dataclass(frozen=True)
class PageConfig:
    page_id: str
    nav_title: str
    title: str
    subtitle: str


@dataclass(frozen=True)
class MatrixProblem:
    name: str
    matrix: NumberMatrix
    vector: NumberVector

    @property
    def size(self) -> int:
        return len(self.vector)


@dataclass(frozen=True)
class RowOperation:
    target_row: int
    pivot_row: int
    factor: float

    def as_text(self) -> str:
        return (
            f"R{self.target_row + 1} <- R{self.target_row + 1} - "
            f"({self.factor:.10g}) * R{self.pivot_row + 1}"
        )


@dataclass(frozen=True)
class EliminationStep:
    step: int
    pivot_column: int
    selected_row: int
    pivot_row: int
    pivot_value: float
    matrix: NumberMatrix
    vector: NumberVector
    operations: list[RowOperation] = field(default_factory=list)

    @property
    def did_swap(self) -> bool:
        return self.selected_row != self.pivot_row


@dataclass(frozen=True)
class BackSubstitutionStep:
    row: int
    numerator: float
    denominator: float
    value: float


@dataclass(frozen=True)
class GaussianResult:
    problem: MatrixProblem
    solution: NumberVector
    determinant: float
    residuals: NumberVector
    residual_norm: float
    elimination_steps: list[EliminationStep]
    back_steps: list[BackSubstitutionStep]
    upper_matrix: NumberMatrix
    transformed_vector: NumberVector
