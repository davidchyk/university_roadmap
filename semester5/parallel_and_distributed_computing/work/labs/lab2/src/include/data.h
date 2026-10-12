#ifndef DATA_H
#define DATA_H

#include <stdbool.h>

typedef struct {
    long long *data;
    int len;
} vec_t;

typedef struct {
    long long *data;
    int shape;
} sqrmatrix_t;

vec_t init_vector(int len);
sqrmatrix_t init_matrix(int shape);

void free_vector(vec_t *vec);
void free_matrix(sqrmatrix_t *matrix);

void value_fill_vector(vec_t *vec, long long value);
void value_fill_matrix(sqrmatrix_t *matrix, long long value);

void scalar_multiply_vector_part(long long scalar, const vec_t *input, vec_t *result, int start, int end);

#endif
