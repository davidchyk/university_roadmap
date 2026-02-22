from __future__ import annotations

def branched_alg(*, r: int | float | complex, x: int | float | complex) -> complex:
    """
    Обчислює функцію y = (4*r - r*x) / (4*x - r*x)

    r, x можуть бути int/float/complex.
    Під час обчислень трактуються як комплексні.
    Обмеження яке в алгоритмі враховується: x != 0 та r != 4.
    """

    if (x == 0) or (r == 4):

        raise ZeroDivisionError("x != 0 and r != 4!")

    t1 = r * x

    g1 = 4*r - t1
    g2 = 4*x - t1

    y = g1 / g2

    return complex(y)