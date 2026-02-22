from __future__ import annotations

def cyclic_alg(*, n: int, p: int) -> int:

    f: int = 0

    if (
        isinstance(n, bool) or not isinstance(n, int)    # Число n строго є типом int (і не bool зокрема)
        or isinstance(p, bool) or not isinstance(p, int) # Число p строго є типом int (і не bool зокрема)
    ):

        raise TypeError("n and p must be int (not float/complex/bool)")

    if (n < 0) or (p < 0):

        raise ValueError("n and p must be non-negative integers (>= 0)")

    for a in range(n+1):

        for b in range(p+1):

            t1 = a**b
            t2 = b**a

            f += t1 + t2

    return f