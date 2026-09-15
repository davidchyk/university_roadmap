from __future__ import annotations

from src.error_analysis import max_estimated_error, max_residual
from src.models import RootInterval, RootResult


def build_short_result(results: list[RootResult]) -> str:
    if not results:
        return "Корені не знайдено на заданому проміжку."

    lines = ["Уточнені корені:"]
    for index, result in enumerate(results, start=1):
        lines.append(
            f"{index}. x = {result.root:.10f}; "
            f"f(x) = {result.function_value:.3e}; "
            f"ітерацій = {result.iterations}"
        )

    lines.append(f"max |f(x)| = {max_residual(results):.3e}")
    lines.append(f"max оцінка похибки = {max_estimated_error(results):.3e}")
    return "\n".join(lines)


def build_full_report(
    function_title: str,
    left: float,
    right: float,
    scan_step: float,
    epsilon: float,
    max_iterations: int,
    intervals: list[RootInterval],
    results: list[RootResult],
) -> str:
    lines: list[str] = [
        "Лабораторна робота N4",
        "Тема: Розв'язання нелінійних рівнянь на комп'ютері",
        "",
        "Метод: метод половинного ділення.",
        f"Рівняння: {function_title}",
        "",
        "Початкові дані:",
        f"Проміжок пошуку: [{left:.10f}; {right:.10f}]",
        f"Крок відокремлення коренів: {scan_step:.10f}",
        f"Точність epsilon: {epsilon:.10g}",
        f"Максимальна кількість ітерацій: {max_iterations}",
        "",
        "Відокремлені проміжки:",
    ]

    if intervals:
        for index, interval in enumerate(intervals, start=1):
            lines.append(f"{index}. {interval.as_text()}")
    else:
        lines.append("Корені на заданому проміжку не відокремлено.")

    lines.extend(["", "Результати уточнення:"])
    if results:
        for index, result in enumerate(results, start=1):
            lines.extend(
                [
                    f"{index}. Проміжок: {result.interval.as_text()}",
                    f"   Корінь: {result.root:.10f}",
                    f"   f(x): {result.function_value:.12e}",
                    f"   Оцінка похибки: {result.estimated_error:.12e}",
                    f"   Кількість ітерацій: {result.iterations}",
                ]
            )
    else:
        lines.append("Корені не уточнювалися, бо проміжки не знайдено.")

    lines.extend(["", "Ітераційні таблиці:"])
    for index, result in enumerate(results, start=1):
        lines.append(f"Корінь {index}, проміжок {result.interval.as_text()}")
        if not result.history:
            lines.append("   Корінь збігається з межею проміжку.")
            continue

        lines.append(
            "   k | a_k | b_k | x_k | f(a_k) | f(x_k) | довжина | похибка"
        )
        for row in result.history:
            lines.append(
                "   "
                f"{row.iteration} | "
                f"{row.left:.10f} | "
                f"{row.right:.10f} | "
                f"{row.midpoint:.10f} | "
                f"{row.f_left:.6e} | "
                f"{row.f_midpoint:.6e} | "
                f"{row.interval_length:.6e} | "
                f"{row.estimated_error:.6e}"
            )

    return "\n".join(lines)
