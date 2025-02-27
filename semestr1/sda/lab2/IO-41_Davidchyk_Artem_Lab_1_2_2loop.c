#include <stdio.h>

int main() {

    int counter = 0;

    int n;
    double sum = 0;
    double first_value = 0.5;
    double second_value = 1;
    double factorial;

    printf("Enter n (2loops): ");
    scanf("%d", &n);

    counter += 7; // 5 операцій присвоювання та 2 виклика стандартних функцій

    for (int i = 1; i <= n; i++) {

        first_value *= 4;
        second_value /= 9;
        factorial = 1;

        for (int j = 1; j <= 2*i; j++) {

            factorial *= j;

            counter += 6; //3 арифметичних операцій, 1 операцій присвоювання, 1 проходження цикла, 1 порівняння

        }

        sum += first_value * second_value / factorial;

        counter += 2; // присвоювання j=1 та останнє порівняння j > 2*i
        counter += 13; // 6 арифметичних операцій, 4 операцій присвоювання, 1 проходження цикла, 1 порівняння

    }

    counter += 3; // присвоювання i = 1, фінальне порівняння коли i > n, фінальний вивід printf

    printf("S = sinh^2(x) = %lf, counter = %d\n", sum, counter);

    return 0;
}