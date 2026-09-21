#ifndef CALCULATOR_H
#define CALCULATOR_H

class Calculator {
public:
    int Add(int lhs, int rhs) const;
    int Sub(int lhs, int rhs) const;
    int Mul(int lhs, int rhs) const;
    double Div(int lhs, int rhs) const;
};

#endif
