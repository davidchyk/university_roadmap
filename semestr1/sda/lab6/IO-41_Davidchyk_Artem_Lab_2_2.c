#include <stdio.h>

int main() {

    int rows, cols;
    int swapped;

    printf("Enter row, col numbers of matrix: ");
    scanf("%d, %d", &rows, &cols);

    int Matrix[rows][cols];

    printf("Enter matrix: \n");

    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j++){
            scanf("%d", &Matrix[i][j]);
        }
    }

    for (int col = 0; col < cols; col++) {

        int left = 0, right = rows - 1;

        do {

            swapped = 0;

            for (int i = left; i < right; i++) {

                if (Matrix[i][col] < Matrix[i + 1][col]) {

                    int temp = Matrix[i][col];
                    Matrix[i][col] = Matrix[i + 1][col];
                    Matrix[i + 1][col] = temp;
                    swapped = 1;
                }
            }

            right--;

            for (int i = right; i > left; i--) {
                if (Matrix[i][col] > Matrix[i - 1][col]) {

                    int temp = Matrix[i][col];
                    Matrix[i][col] = Matrix[i - 1][col];
                    Matrix[i - 1][col] = temp;
                    swapped = 1;
                }
            }

            left++;

        } while (swapped);

    }

    printf("\nSorted matrix: \n");

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", Matrix[i][j]);
        }

        printf("\n");
    }

    printf("\n");

    return 0;

}