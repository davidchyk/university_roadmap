from __future__ import annotations

from src.models import EliminationStep, GaussianResult, MatrixProblem, NumberMatrix, NumberVector


def build_short_result(result: GaussianResult) -> str:
    lines = ["Розв'язок:"]
    for index, value in enumerate(result.solution, start=1):
        lines.append(f"x{index} = {value:.10f}")

    lines.append(f"det(A) = {result.determinant:.10g}")
    lines.append(f"max |Ax - b| = {result.residual_norm:.3e}")
    return "\n".join(lines)


def build_full_report(result: GaussianResult) -> str:
    problem = result.problem
    lines: list[str] = [
        "Лабораторна робота N5",
        "Тема: Розв'язання систем лінійних алгебраїчних рівнянь",
        "",
        "Метод: метод Гауса з вибором головного елемента.",
        f"Система: {problem.name}",
        f"Розмірність: {problem.size} x {problem.size}",
        "",
        "Початкова розширена матриця:",
        *_format_augmented(problem.matrix, problem.vector),
        "",
        "Прямий хід:",
    ]

    for step in result.elimination_steps:
        lines.extend(_format_step(step))

    lines.extend(
        [
            "",
            "Верхньотрикутна система:",
            *_format_augmented(result.upper_matrix, result.transformed_vector),
            "",
            "Зворотний хід:",
        ]
    )

    for step in result.back_steps:
        lines.append(
            f"x{step.row + 1} = {step.numerator:.12g} / "
            f"{step.denominator:.12g} = {step.value:.12g}"
        )

    lines.extend(["", "Розв'язок:"])
    for index, value in enumerate(result.solution, start=1):
        lines.append(f"x{index} = {value:.12g}")

    lines.extend(
        [
            "",
            "Перевірка Ax - b:",
        ]
    )
    for index, value in enumerate(result.residuals, start=1):
        lines.append(f"r{index} = {value:.12e}")

    lines.extend(
        [
            "",
            f"max |Ax - b| = {result.residual_norm:.12e}",
            f"det(A) = {result.determinant:.12g}",
        ]
    )
    return "\n".join(lines)


def format_matrix_for_display(matrix: NumberMatrix, vector: NumberVector | None = None) -> str:
    return "\n".join(_format_augmented(matrix, vector) if vector is not None else _format_matrix(matrix))


def _format_step(step: EliminationStep) -> list[str]:
    lines = [
        "",
        f"Крок {step.step}. Стовпець {step.pivot_column + 1}; "
        f"вибраний рядок R{step.selected_row + 1}; "
        f"головний елемент = {step.pivot_value:.12g}.",
    ]
    if step.did_swap:
        lines.append(f"Перестановка: R{step.pivot_row + 1} <-> R{step.selected_row + 1}.")
    else:
        lines.append("Перестановка рядків не потрібна.")

    if step.operations:
        lines.append("Операції:")
        lines.extend(f"  {operation.as_text()}" for operation in step.operations)
    else:
        lines.append("Операцій занулення немає.")

    lines.append("Матриця після кроку:")
    lines.extend(_format_augmented(step.matrix, step.vector))
    return lines


def _format_augmented(matrix: NumberMatrix, vector: NumberVector | None) -> list[str]:
    rows: list[str] = []
    for row_index, row in enumerate(matrix):
        coefficients = "  ".join(f"{value:>13.6g}" for value in row)
        if vector is None:
            rows.append(f"[ {coefficients} ]")
        else:
            rows.append(f"[ {coefficients} | {vector[row_index]:>13.6g} ]")
    return rows


def _format_matrix(matrix: NumberMatrix) -> list[str]:
    return _format_augmented(matrix, None)
