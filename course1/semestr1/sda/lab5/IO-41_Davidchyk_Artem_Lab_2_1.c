#include <stdio.h>

int main() {

    double x;
    int row, col;

    printf("Enter row, col numbers of matrix: ");
    scanf("%d, %d", &row, &col);

    double Matrix[row][col];

    printf("Enter matrix: \n");

    for (int i = 0; i < row; i++){
        for (int j = 0; j < col; j++){
            scanf("%lf", &Matrix[i][j]);
        }
    }

    printf("Enter x number: ");
    scanf("%lf", &x);

    for (int i = 0; i < row; i++) {

        int L = 0;
        int R = col-1;

        while (L < R) {

            int mid = (R + L) / 2;

            if (Matrix[i][mid] < x) L = mid+1;
            else R = mid;

        }

        if (Matrix[i][R] == x) printf("Element %.2lf is in row %d at position %d\n", x, i, R);
        else printf("Element %.2lf is not in row %d\n", x, i);

    }

    return 0;

}