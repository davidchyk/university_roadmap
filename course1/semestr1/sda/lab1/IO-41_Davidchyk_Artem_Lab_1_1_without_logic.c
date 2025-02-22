#include <stdio.h>

int main() {
    
    double x;

    printf("Enter value for x: ");
    scanf("%lf", &x);

    if (x >= 0) {

        if (x >= 11) {
            double result = -pow(x, 3) / 7 + 10;
            printf("y = %lf\n", result);

        }

        else if (x < 7) {
            double result = -6 * pow(x, 2) + 8;
            printf("y = %lf\n", result);

        }

        else {

            printf("no value\n");
        }

    }

    else if (x <= -10) {

        double result = -pow(x, 3) / 7 + 10;
        printf("y = %lf\n", result);

    }

    else {

        printf("no value\n");
    }

    return 0;

}