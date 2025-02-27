def calculate_minimized_expression(A: set, B: set, C: set, U: set) -> set:

    not_A = U.difference(A)
    not_B = U.difference(B)
    not_C = U.difference(C)

    R = not_A.union(not_B)
    D = R.union(not_C)

    return D