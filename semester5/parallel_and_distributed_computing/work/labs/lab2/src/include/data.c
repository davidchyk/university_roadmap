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

void value_fill_vector(vec_t *vec, long long value) {

    if (!vector_is_valid(vec)) {
        return;
    }

    for (int i = 0; i < vec->len; ++i) {
        vec->data[i] = value;
    }
}

void value_fill_matrix(sqrmatrix_t *matrix, long long value) {

    if (!matrix_is_valid(matrix)) {
        return;
    }

    const size_t element_count =
        (size_t)matrix->shape * (size_t)matrix->shape;
    for (size_t i = 0; i < element_count; ++i) {
        matrix->data[i] = value;
    }
}

void scalar_multiply_vector_part(long long scalar, const vec_t *input, vec_t *result, int start, int end) {

    for (int j = start; j < end; j++) {

        result->data[j] = scalar * input->data[j];

    }

}
