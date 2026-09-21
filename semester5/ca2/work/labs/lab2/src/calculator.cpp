#include "calculator.h"

#include <stdexcept>

int Calculator::Add(int lhs, int rhs) const {
    return lhs + rhs;
}

int Calculator::Sub(int lhs, int rhs) const {
    return lhs - rhs;
}

int Calculator::Mul(int lhs, int rhs) const {
    return lhs * rhs;
}

double Calculator::Div(int lhs, int rhs) const {
    if (rhs == 0) {
        throw std::invalid_argument("division by zero");
    }
    return static_cast<double>(lhs) / rhs;
}
