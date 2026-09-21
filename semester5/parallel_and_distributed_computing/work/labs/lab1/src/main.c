/*

Паралельні та розподілені обчислення
6 номер у списку групи
Лабораторна робота №1.2: Потоки в БІБЛІОТЕЦІ WinАРІ (PThread)
F1 (1.6): MD = (B * C) * (MA * ME)
F2 (2.6): MG = TRANS(MK) * (MH * MF)
F3 (3.6): O = MAX(MP * MR) * V
Давидчук Артем Миколайович, група ІО-41
09.21.2026

*/

#define _POSIX_C_SOURCE 200809L

#include <stdbool.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "include/data.h"

typedef struct {
    int n;
    int fill_value;
    bool random_fill;
} function_args_t;

static bool read_fill_value(function_args_t *args, int function_number) {

    if (args->random_fill) {
        return true;
    }

    printf("T%d: enter one integer to fill F%d data: ",
           function_number, function_number);
    fflush(stdout);
    const bool input_is_valid = scanf("%d", &args->fill_value) == 1;

    if (!input_is_valid) {
        fprintf(stderr, "F%d: an integer was expected\n", function_number);
    }

    return input_is_valid;
}

static void fill_vector(vec_t *vector, const function_args_t *args) {

    if (args->random_fill) {
        random_fill_vector(vector);
    } else {
        value_fill_vector(vector, args->fill_value);
    }
}

static void fill_matrix(sqrmatrix_t *matrix, const function_args_t *args) {

    if (args->random_fill) {
        random_fill_matrix(matrix);
    } else {
        value_fill_matrix(matrix, args->fill_value);
    }
}

static void print_vector(const char *name, const vec_t *vector) {

    printf("%s = [", name);
    for (int i = 0; i < vector->len; ++i) {
        printf("%d%s", vector->data[i], i + 1 == vector->len ? "" : " ");
    }
    printf("]\n");
}

static void print_matrix(const char *name, const sqrmatrix_t *matrix) {

    printf("%s =\n", name);
    for (int row = 0; row < matrix->shape; ++row) {
        for (int column = 0; column < matrix->shape; ++column) {
            printf("%d%s",
                   matrix->data[(size_t)row * matrix->shape + column],
                   column + 1 == matrix->shape ? "" : " ");
        }
        printf("\n");
    }
}

// F1 (1.6): MD = (B * C) * (MA * ME)
void *F1(void *argument) {

    function_args_t *args = argument;

    if (!read_fill_value(args, 1)) {
        return NULL;
    }

    vec_t B = init_vector(args->n);
    vec_t C = init_vector(args->n);
    sqrmatrix_t MA = init_matrix(args->n);
    sqrmatrix_t ME = init_matrix(args->n);

    if (B.data == NULL || C.data == NULL ||
        MA.data == NULL || ME.data == NULL) {
        fprintf(stderr, "F1: memory allocation error\n");
        free_vector(&B);
        free_vector(&C);
        free_matrix(&MA);
        free_matrix(&ME);
        return NULL;
    }

    fill_vector(&B, args);
    fill_vector(&C, args);
    fill_matrix(&MA, args);
    fill_matrix(&ME, args);

    const int scalar = vectors_multiply(&B, &C);
    sqrmatrix_t matrix_product = matrices_multiply(&MA, &ME);
    sqrmatrix_t MD = scalar_multiply_matrix(scalar, &matrix_product);

    if (matrix_product.data == NULL || MD.data == NULL) {
        fprintf(stderr, "F1: calculation error\n");
    } else if (args->n == 3) {
        print_matrix("F1: MD", &MD);
    } else {
        printf("F1: MD calculated\n");
    }

    free_vector(&B);
    free_vector(&C);
    free_matrix(&MA);
    free_matrix(&ME);
    free_matrix(&matrix_product);
    free_matrix(&MD);

    return NULL;
}

// F2 (2.6): MG = TRANS(MK) * (MH * MF)
void *F2(void *argument) {

    function_args_t *args = argument;

    if (!read_fill_value(args, 2)) {
        return NULL;
    }

    sqrmatrix_t MK = init_matrix(args->n);
    sqrmatrix_t MH = init_matrix(args->n);
    sqrmatrix_t MF = init_matrix(args->n);

    if (MK.data == NULL || MH.data == NULL || MF.data == NULL) {
        fprintf(stderr, "F2: memory allocation error\n");
        free_matrix(&MK);
        free_matrix(&MH);
        free_matrix(&MF);
        return NULL;
    }

    fill_matrix(&MK, args);
    fill_matrix(&MH, args);
    fill_matrix(&MF, args);

    sqrmatrix_t transposed_MK = transpose_matrix(&MK);
    sqrmatrix_t matrix_product = matrices_multiply(&MH, &MF);
    sqrmatrix_t MG = matrices_multiply(&transposed_MK, &matrix_product);

    if (transposed_MK.data == NULL || matrix_product.data == NULL ||
        MG.data == NULL) {
        fprintf(stderr, "F2: calculation error\n");
    } else if (args->n == 3) {
        print_matrix("F2: MG", &MG);
    } else {
        printf("F2: MG calculated\n");
    }

    free_matrix(&MK);
    free_matrix(&MH);
    free_matrix(&MF);
    free_matrix(&transposed_MK);
    free_matrix(&matrix_product);
    free_matrix(&MG);

    return NULL;
}

// F3 (3.6): O = MAX(MP * MR) * V
void *F3(void *argument) {

    function_args_t *args = argument;

    if (!read_fill_value(args, 3)) {
        return NULL;
    }

    sqrmatrix_t MP = init_matrix(args->n);
    sqrmatrix_t MR = init_matrix(args->n);
    vec_t V = init_vector(args->n);

    if (MP.data == NULL || MR.data == NULL || V.data == NULL) {
        fprintf(stderr, "F3: memory allocation error\n");
        free_matrix(&MP);
        free_matrix(&MR);
        free_vector(&V);
        return NULL;
    }

    fill_matrix(&MP, args);
    fill_matrix(&MR, args);
    fill_vector(&V, args);

    sqrmatrix_t matrix_product = matrices_multiply(&MP, &MR);
    int maximum;
    vec_t O = {NULL, 0};

    if (matrix_product.data != NULL &&
        matrix_maximum(&matrix_product, &maximum)) {
        O = scalar_multiply_vector(maximum, &V);
    }

    if (matrix_product.data == NULL || O.data == NULL) {
        fprintf(stderr, "F3: calculation error\n");
    } else if (args->n == 3) {
        print_vector("F3: O", &O);
    } else {
        printf("F3: O calculated\n");
    }

    free_matrix(&MP);
    free_matrix(&MR);
    free_vector(&V);
    free_matrix(&matrix_product);
    free_vector(&O);

    return NULL;
}

int main(void) {

    int N;

    // Inputing

    printf("Enter N (3 or 1000): ");
    if (scanf("%d", &N) != 1 || (N != 3 && N != 1000)) {
        fprintf(stderr, "Error: N must be 3 or 1000\n");
        return EXIT_FAILURE;
    }

    function_args_t args[3];
    for (int i = 0; i < 3; ++i) {
        args[i].n = N;
        args[i].fill_value = 0;
        args[i].random_fill = N == 1000;
    }

    if (N == 1000) {
        srand((unsigned int)time(NULL));
        printf("F1, F2 and F3 data will be filled randomly\n");
    }

    // Counting

    printf("Starting:\n");

    pthread_t T1, T2, T3;
    struct timespec start_time;
    struct timespec end_time;

    if (clock_gettime(CLOCK_MONOTONIC, &start_time) != 0) {
        perror("clock_gettime");
        return EXIT_FAILURE;
    }

    const int t1_status = pthread_create(&T1, NULL, F1, &args[0]);
    const int t2_status = pthread_create(&T2, NULL, F2, &args[1]);
    const int t3_status = pthread_create(&T3, NULL, F3, &args[2]);

    if (t1_status == 0) {
        pthread_join(T1, NULL);
    }
    if (t2_status == 0) {
        pthread_join(T2, NULL);
    }
    if (t3_status == 0) {
        pthread_join(T3, NULL);
    }

    if (clock_gettime(CLOCK_MONOTONIC, &end_time) != 0) {
        perror("clock_gettime");
        return EXIT_FAILURE;
    }

    const double elapsed_seconds =
        (double)(end_time.tv_sec - start_time.tv_sec) +
        (double)(end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;

    if (t1_status != 0 || t2_status != 0 || t3_status != 0) {
        fprintf(stderr,
                "Thread creation error: T1=%d, T2=%d, T3=%d\n",
                t1_status, t2_status, t3_status);
        return EXIT_FAILURE;
    }

    printf("Completed\n");
    printf("Threads computation time: %.6f seconds\n", elapsed_seconds);

    return EXIT_SUCCESS;
}
