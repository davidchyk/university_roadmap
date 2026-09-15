from __future__ import annotations

from math import isfinite

from src.models import (
    BackSubstitutionStep,
    EliminationStep,
    GaussianResult,
    MatrixProblem,
    NumberMatrix,
    NumberVector,
    RowOperation,
)


DEFAULT_PROBLEM = MatrixProblem(
    name="Варіант з фото",
    matrix=[
        [0.63, 1.00, 0.71, 0.34],
        [1.17, 0.18, -0.65, 0.71],
        [2.71, -0.75, 1.17, -2.35],
        [3.58, 0.21, -3.45, -1.18],
    ],
    vector=[2.08, 0.17, 1.28, 0.05],
)


def build_default_problem() -> MatrixProblem:
    return MatrixProblem(
        name=DEFAULT_PROBLEM.name,
        matrix=clone_matrix(DEFAULT_PROBLEM.matrix),
        vector=DEFAULT_PROBLEM.vector[:],
    )


def clone_matrix(matrix: NumberMatrix) -> NumberMatrix:
    return [row[:] for row in matrix]


def validate_problem(problem: MatrixProblem) -> None:
    size = problem.size
    if size < 2:
        raise ValueError("Система має містити щонайменше 2 рівняння.")
    if size > 10:
        raise ValueError("Для зручного GUI підтримується розмір до 10.")
    if len(problem.matrix) != size:
        raise ValueError("Кількість рядків матриці має збігатися з розміром вектора b.")

    for row_index, row in enumerate(problem.matrix, start=1):
        if len(row) != size:
            raise ValueError(f"Рядок {row_index} матриці має містити {size} коефіцієнтів.")
        for value in row:
            if not isfinite(value):
                raise ValueError("Усі коефіцієнти мають бути скінченними числами.")

    for value in problem.vector:
        if not isfinite(value):
            raise ValueError("Вектор вільних членів має містити скінченні числа.")


def solve_gauss_partial_pivot(
    problem: MatrixProblem,
    tolerance: float = 1e-12,
) -> GaussianResult:
    validate_problem(problem)
    if tolerance <= 0:
        raise ValueError("Допуск має бути додатним.")

    size = problem.size
    matrix = clone_matrix(problem.matrix)
    vector = problem.vector[:]
    determinant_sign = 1.0
    elimination_steps: list[EliminationStep] = []

    for column in range(size - 1):
        selected_row = max(range(column, size), key=lambda row: abs(matrix[row][column]))
        pivot_value = matrix[selected_row][column]
        if abs(pivot_value) <= tolerance:
            raise ValueError(
                f"Система вироджена або майже вироджена: "
                f"нульовий головний елемент у стовпці {column + 1}."
            )

        if selected_row != column:
            matrix[column], matrix[selected_row] = matrix[selected_row], matrix[column]
            vector[column], vector[selected_row] = vector[selected_row], vector[column]
            determinant_sign *= -1.0

        operations: list[RowOperation] = []
        pivot_value = matrix[column][column]

        for row in range(column + 1, size):
            factor = matrix[row][column] / pivot_value
            operations.append(RowOperation(row, column, factor))
            matrix[row][column] = 0.0

            for inner_column in range(column + 1, size):
                matrix[row][inner_column] -= factor * matrix[column][inner_column]
                if abs(matrix[row][inner_column]) < tolerance:
                    matrix[row][inner_column] = 0.0

            vector[row] -= factor * vector[column]
            if abs(vector[row]) < tolerance:
                vector[row] = 0.0

        elimination_steps.append(
            EliminationStep(
                step=column + 1,
                pivot_column=column,
                selected_row=selected_row,
                pivot_row=column,
                pivot_value=pivot_value,
                matrix=clone_matrix(matrix),
                vector=vector[:],
                operations=operations,
            )
        )

    last_pivot = matrix[-1][-1]
    if abs(last_pivot) <= tolerance:
        raise ValueError("Система не має єдиного розв'язку: останній діагональний елемент нульовий.")

    solution = [0.0 for _ in range(size)]
    back_steps: list[BackSubstitutionStep] = []
    for row in range(size - 1, -1, -1):
        known_sum = sum(matrix[row][column] * solution[column] for column in range(row + 1, size))
        numerator = vector[row] - known_sum
        denominator = matrix[row][row]
        if abs(denominator) <= tolerance:
            raise ValueError(f"Неможливо виконати зворотний хід у рядку {row + 1}.")

        solution[row] = numerator / denominator
        back_steps.append(
            BackSubstitutionStep(
                row=row,
                numerator=numerator,
                denominator=denominator,
                value=solution[row],
            )
        )

    determinant = determinant_sign
    for diagonal_index in range(size):
        determinant *= matrix[diagonal_index][diagonal_index]

    residuals = compute_residuals(problem.matrix, solution, problem.vector)
    residual_norm = max((abs(value) for value in residuals), default=0.0)

    return GaussianResult(
        problem=problem,
        solution=solution,
        determinant=determinant,
        residuals=residuals,
        residual_norm=residual_norm,
        elimination_steps=elimination_steps,
        back_steps=list(reversed(back_steps)),
        upper_matrix=clone_matrix(matrix),
        transformed_vector=vector[:],
    )


def compute_residuals(
    matrix: NumberMatrix,
    solution: NumberVector,
    vector: NumberVector,
) -> NumberVector:
    residuals: NumberVector = []
    for row, right_side in zip(matrix, vector):
        actual = sum(coefficient * value for coefficient, value in zip(row, solution))
        residuals.append(actual - right_side)
    return residuals


def rounded_solution(solution: NumberVector, digits: int = 4) -> NumberVector:
    return [round(value, digits) for value in solution]
