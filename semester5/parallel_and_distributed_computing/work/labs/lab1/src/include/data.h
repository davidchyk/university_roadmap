#ifndef DATA_H
#define DATA_H

#include <stdbool.h>

/* Elements of a matrix are stored row by row (row-major order). */
typedef struct {
    int *data;
    int len;
} vec_t;

typedef struct {
    int *data;
    int shape;
} sqrmatrix_t;

/* Creation. On an invalid size or allocation failure, an empty object is returned. */
vec_t init_vector(int len);
sqrmatrix_t init_matrix(int shape);

/* Release owned memory and reset the object to its empty state. */
void free_vector(vec_t *vec);
void free_matrix(sqrmatrix_t *matrix);

/* Filling. Random values are generated in the range [0, 9]. */
void value_fill_vector(vec_t *vec, int value);
void random_fill_vector(vec_t *vec);
void value_fill_matrix(sqrmatrix_t *matrix, int value);
void random_fill_matrix(sqrmatrix_t *matrix);

/* Vector dot product. Returns 0 for invalid vectors or different lengths. */
int vectors_multiply(const vec_t *left, const vec_t *right);

/* Operations returning new objects. The caller must free their result. */
vec_t scalar_multiply_vector(int scalar, const vec_t *vec);
sqrmatrix_t matrices_multiply(const sqrmatrix_t *left,
                              const sqrmatrix_t *right);
sqrmatrix_t scalar_multiply_matrix(int scalar, const sqrmatrix_t *matrix);
sqrmatrix_t transpose_matrix(const sqrmatrix_t *matrix);

/* Writes the largest element to result. Returns false for an invalid matrix. */
bool matrix_maximum(const sqrmatrix_t *matrix, int *result);

#endif
