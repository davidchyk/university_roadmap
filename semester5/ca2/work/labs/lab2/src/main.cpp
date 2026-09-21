#include "calculator.h"

#include <iostream>

int main() {
    const Calculator calculator;

    std::cout << "2 + 3 = " << calculator.Add(2, 3) << '\n';
    std::cout << "5 - 1 = " << calculator.Sub(5, 1) << '\n';
    std::cout << "4 * 2 = " << calculator.Mul(4, 2) << '\n';
    std::cout << "9 / 3 = " << calculator.Div(9, 3) << '\n';

    return 0;
}
