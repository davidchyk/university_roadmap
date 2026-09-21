#include "data.h"

#include <stdint.h>
#include <stdlib.h>

static bool vector_is_valid(const vec_t *vec) {

    return vec != NULL && vec->data != NULL && vec->len > 0;
}

static bool matrix_is_valid(const sqrmatrix_t *matrix) {

    return matrix != NULL && matrix->data != NULL && matrix->shape > 0;
}

vec_t init_vector(int len) {

    vec_t vec = {NULL, 0};

    if (len <= 0 || (size_t)len > SIZE_MAX / sizeof(*vec.data)) {
        return vec;
    }

    vec.data = malloc((size_t)len * sizeof(*vec.data));
    if (vec.data != NULL) {
        vec.len = len;
    }

    return vec;
}

sqrmatrix_t init_matrix(int shape) {

    sqrmatrix_t matrix = {NULL, 0};

    if (shape <= 0 || (size_t)shape > SIZE_MAX / (size_t)shape) {
        return matrix;
    }

    const size_t element_count = (size_t)shape * (size_t)shape;
    if (element_count > SIZE_MAX / sizeof(*matrix.data)) {
        return matrix;
    }

    matrix.data = malloc(element_count * sizeof(*matrix.data));
    if (matrix.data != NULL) {
        matrix.shape = shape;
    }

    return matrix;
}

void free_vector(vec_t *vec) {

    if (vec == NULL) {
        return;
    }

    free(vec->data);
    vec->data = NULL;
    vec->len = 0;
}

void free_matrix(sqrmatrix_t *matrix) {

    if (matrix == NULL) {
        return;
    }

    free(matrix->data);
    matrix->data = NULL;
    matrix->shape = 0;
}

void value_fill_vector(vec_t *vec, int value) {

    if (!vector_is_valid(vec)) {
        return;
    }

    for (int i = 0; i < vec->len; ++i) {
        vec->data[i] = value;
    }
}

void random_fill_vector(vec_t *vec) {

    if (!vector_is_valid(vec)) {
        return;
    }

    for (int i = 0; i < vec->len; ++i) {
        vec->data[i] = rand() % 10;
    }
}

void value_fill_matrix(sqrmatrix_t *matrix, int value) {

    if (!matrix_is_valid(matrix)) {
        return;
    }

    const size_t element_count =
        (size_t)matrix->shape * (size_t)matrix->shape;
    for (size_t i = 0; i < element_count; ++i) {
        matrix->data[i] = value;
    }
}

void random_fill_matrix(sqrmatrix_t *matrix) {

    if (!matrix_is_valid(matrix)) {
        return;
    }

    const size_t element_count =
        (size_t)matrix->shape * (size_t)matrix->shape;
    for (size_t i = 0; i < element_count; ++i) {
        matrix->data[i] = rand() % 10;
    }
}

int vectors_multiply(const vec_t *left, const vec_t *right) {

    if (!vector_is_valid(left) || !vector_is_valid(right) ||
        left->len != right->len) {
        return 0;
    }

    int result = 0;
    for (int i = 0; i < left->len; ++i) {
        result += left->data[i] * right->data[i];
    }

    return result;
}

vec_t scalar_multiply_vector(int scalar, const vec_t *vec)
{
    if (!vector_is_valid(vec)) {
        return (vec_t){NULL, 0};
    }

    vec_t result = init_vector(vec->len);
    if (result.data == NULL) {
        return result;
    }

    for (int i = 0; i < vec->len; ++i) {
        result.data[i] = scalar * vec->data[i];
    }

    return result;
}

sqrmatrix_t matrices_multiply(const sqrmatrix_t *left, const sqrmatrix_t *right) {

    if (!matrix_is_valid(left) || !matrix_is_valid(right) ||
        left->shape != right->shape) {
        return (sqrmatrix_t){NULL, 0};
    }

    const int n = left->shape;
    sqrmatrix_t result = init_matrix(n);
    if (result.data == NULL) {
        return result;
    }

    for (int row = 0; row < n; ++row) {
        for (int column = 0; column < n; ++column) {
            int sum = 0;
            for (int k = 0; k < n; ++k) {
                sum += left->data[(size_t)row * n + k] *
                       right->data[(size_t)k * n + column];
            }
            result.data[(size_t)row * n + column] = sum;
        }
    }

    return result;
}

sqrmatrix_t scalar_multiply_matrix(int scalar, const sqrmatrix_t *matrix) {

    if (!matrix_is_valid(matrix)) {
        return (sqrmatrix_t){NULL, 0};
    }

    sqrmatrix_t result = init_matrix(matrix->shape);
    if (result.data == NULL) {
        return result;
    }

    const size_t element_count =
        (size_t)matrix->shape * (size_t)matrix->shape;
    for (size_t i = 0; i < element_count; ++i) {
        result.data[i] = scalar * matrix->data[i];
    }

    return result;
}

sqrmatrix_t transpose_matrix(const sqrmatrix_t *matrix) {
    if (!matrix_is_valid(matrix)) {
        return (sqrmatrix_t){NULL, 0};
    }

    const int n = matrix->shape;
    sqrmatrix_t result = init_matrix(n);
    if (result.data == NULL) {
        return result;
    }

    for (int row = 0; row < n; ++row) {
        for (int column = 0; column < n; ++column) {
            result.data[(size_t)column * n + row] = matrix->data[(size_t)row * n + column];
        }
    }

    return result;
}

bool matrix_maximum(const sqrmatrix_t *matrix, int *result) {

    if (!matrix_is_valid(matrix) || result == NULL) {
        return false;
    }

    int maximum = matrix->data[0];
    const size_t element_count =
        (size_t)matrix->shape * (size_t)matrix->shape;
    for (size_t i = 1; i < element_count; ++i) {
        if (matrix->data[i] > maximum) {
            maximum = matrix->data[i];
        }
    }

    *result = maximum;
    return true;
}
