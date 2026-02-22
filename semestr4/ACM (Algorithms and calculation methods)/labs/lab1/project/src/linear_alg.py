from __future__ import annotations

def linear_alg(*, a: int | float | complex, b: int | float | complex, c: int | float | complex, d: int | float | complex) -> complex:
    """
    Обчислює функцію Y1 = (d*a)^b + (b*c)^(1/d)

    a, b, c, d можуть бути int/float/complex.
    Під час обчислень трактуються як комплексні.
    Обмеження яке в алгоритмі не враховується: d != 0.
    """

    t1 = d * a
    t2 = b * c

    p = 1 / d

    g1 = t1 ** b
    g2 = t2 ** p

    Y1 = g1 + g2

    return complex(Y1)