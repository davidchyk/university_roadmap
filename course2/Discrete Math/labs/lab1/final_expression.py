def calculate_final_expression(A: set, B: set, U: set) -> set:

    X = U.difference(A)
    Y = U.difference(B)

    Z = X.intersection(Y)

    return X, Y, Z