def calculate_initial_expression(A: set, B: set, C: set, U: set) -> set:

    not_A = U.difference(A)
    not_B = U.difference(B)
    not_C = U.difference(C)

    R5 = not_A.intersection(B)
    R6 = not_B.intersection(C)
    R7 = not_A.union(not_B)
    R8 = R5.union(R6)
    R9 = R8.union(not_C)
    D = R7.union(R9)

    return D