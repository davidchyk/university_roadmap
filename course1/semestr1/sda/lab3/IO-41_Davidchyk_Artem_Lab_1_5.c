#include <stdio.h>

int main() {

    int n;

    int negative_coords = 1;
    int positive_coords = -1;

    printf("Enter n number of matrix: ");
    scanf("%d", &n);

    double Matrix[n][n];

    printf("Enter matrix: \n");

    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            scanf("%lf", &Matrix[i][j]);
        }
    }

    for (int i = 0; i < n; i++) {

        if (Matrix[i][i] < 0 && negative_coords == 1) negative_coords = i;
        if (Matrix[i][i] > 0) positive_coords = i;

    }

    if ((negative_coords == 1) || (positive_coords == -1)) {

        printf("\nThere is no negative or positive value in matrix\n");

    }

    else {

        float negative = Matrix[negative_coords][negative_coords];

        Matrix[negative_coords][negative_coords] = Matrix[positive_coords][positive_coords];
        Matrix[positive_coords][positive_coords] = negative;

        printf("\nResult matrix: \n");

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                printf("%.2lf   ", Matrix[i][j]);
            }

            printf("\n");

        }

    }

    return 0;

}