#include <stdio.h>

int main() {

    int counter = 0;

    int n;
    double Sum = 0;
    double first_value = 0.5;
    double second_value = 1;
    double factorial = 1;

    printf("Enter n (Dynamic Programming): ");
    scanf("%d", &n);

    counter += 7; //5 операцій присвоювання та 2 виклика стандартних функцій

    for (int i = 1; i <= n; i++) {

        first_value *= 4;
        second_value /= 9;
        factorial *= (2*i-1) * 2*i;

        Sum += first_value * second_value / factorial;
    
        counter += 17; //11 арифметичних операцій, 4 операції присвоювання, 1 проходження цикла, 1 порівняння

    }

    counter += 3; // присвоєння int i = 1; Ще одне фінальне порівняння коли i > n; виклик фінального printf

    printf("S = sinh^2(x) = %.7lf, counter = %d\n", Sum, counter);

    return 0;

}