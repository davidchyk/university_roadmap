/*

Паралельні та розподілені обчислення
17 варіант за таблицею варіантів
Лабораторна робота №2.1: Синхронізація потоків
Давидчук Артем Миколайович, група ІО-41
12.10.2026

*/

#define _POSIX_C_SOURCE 200809L

#include <stdbool.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <limits.h>
#include <errno.h>

#include <stdatomic.h>
#include <semaphore.h>

#include "include/data.h"

static pthread_mutex_t console_mutex = PTHREAD_MUTEX_INITIALIZER;
static atomic_llong min_b;

static pthread_barrier_t input_ready;
static pthread_barrier_t intermediate_ready;
static sem_t finished;
static struct timespec start_time, end_time;

typedef struct shared_memory {

    int N;
    vec_t B, Q, E;
    sqrmatrix_t MR, MM, MO;
    long long d;

    // temp

    vec_t V;
    sqrmatrix_t MX;

} shared_memory;

void* F1(void* _) {

    shared_memory* sm = _;
    long long MR_fill_number, Q_fill_number;
    long long local_min = LLONG_MAX;

    pthread_mutex_lock(&console_mutex);

    printf("Input element for MR matrix: ");
    fflush(stdout);
    if (scanf("%lld", &MR_fill_number) != 1) {
        fprintf(stderr, "Invalid input for MR_fill_number\n");
        exit(EXIT_FAILURE);
    }

    value_fill_matrix(&sm->MR, MR_fill_number);

    printf("Input element for Q vector: ");
    fflush(stdout);
    if (scanf("%lld", &Q_fill_number) != 1) {
        fprintf(stderr, "Invalid input for Q_fill_number\n");
        exit(EXIT_FAILURE);
    }

    value_fill_vector(&sm->Q, Q_fill_number);

    pthread_mutex_unlock(&console_mutex);

    // Усі дані введено. Один учасник фіксує початок часу.
    int barrier_status = pthread_barrier_wait(&input_ready);
    if (barrier_status != 0 && barrier_status != PTHREAD_BARRIER_SERIAL_THREAD) {
        fprintf(stderr, "Input barrier error: %d\n", barrier_status);
        exit(EXIT_FAILURE);
    }
    if (barrier_status == PTHREAD_BARRIER_SERIAL_THREAD) {
        if (clock_gettime(CLOCK_MONOTONIC, &start_time) != 0) {
            perror("clock_gettime");
            exit(EXIT_FAILURE);
        }
    }
    // Не починати обчислення, доки start_time не записано.
    pthread_barrier_wait(&input_ready);

    int start = 0;
    int end = sm->N / 4;

    for (int j = start; j < end; j++) {
        long long sum = 0;

        for (int i = 0; i < sm->N; i++) {
            sum += sm->B.data[i]
                 * sm->MR.data[(size_t)i * sm->N + j];
        }

        sm->V.data[j] = sum;
    }

    for (int j = start; j < end; j++) {

        for (int i = 0; i < sm->N; i++) {

            long long sum = 0;

            for (int k = 0; k < sm->N; k++) {

                sum += sm->MM.data[(size_t)i * sm->N + k]
                     * sm->MO.data[(size_t)k * sm->N + j];

            }

            sm->MX.data[(size_t)i * sm->N + j] = sum;
        }

    }

    for (int i = start; i < end; i++) {
        if (sm->B.data[i] < local_min)
            local_min = sm->B.data[i];
    }

    long long current = atomic_load(&min_b);

    while (local_min < current) {
        if (atomic_compare_exchange_weak(
                &min_b, &current, local_min)) {
            break;
        }
    }

    pthread_barrier_wait(&intermediate_ready);

    long long minimum = atomic_load(&min_b);

    for (int j = start; j < end; j++) {

        long long sum = 0;

        for (int k = 0; k < sm->N; k++) {

            sum += sm->V.data[k] * sm->MX.data[(size_t)k * sm->N + j];

        }

        sm->E.data[j] = sum + minimum * sm->Q.data[j] * sm->d;

    }

    for (int i = 0; i < 3; i++) {
        while (sem_wait(&finished) == -1) {
            if (errno != EINTR) {
                perror("sem_wait");
                exit(EXIT_FAILURE);
            }
        }
    }

    if (clock_gettime(CLOCK_MONOTONIC, &end_time) != 0) {
        perror("clock_gettime");
        exit(EXIT_FAILURE);
    }
    pthread_mutex_lock(&console_mutex);

    printf("Completed. E result:\n[");

    for (int i = 0; i < sm->N; i++) {

        printf("%lld", sm->E.data[i]);
        if (i != sm->N-1) printf(", ");

    }

    printf("]\n");
    pthread_mutex_unlock(&console_mutex);

    return NULL;

}

void* F2(void* _) {

    shared_memory* sm = _;
    long long MM_fill_number, B_fill_number;
    long long local_min = LLONG_MAX;

    pthread_mutex_lock(&console_mutex);

    printf("Input element for MM matrix: ");
    fflush(stdout);
    if (scanf("%lld", &MM_fill_number) != 1) {
        fprintf(stderr, "Invalid input for MM_fill_number\n");
        exit(EXIT_FAILURE);
    }

    value_fill_matrix(&sm->MM, MM_fill_number);

    printf("Input element for B vector: ");
    fflush(stdout);
    if (scanf("%lld", &B_fill_number) != 1) {
        fprintf(stderr, "Invalid input for B_fill_number\n");
        exit(EXIT_FAILURE);
    }

    value_fill_vector(&sm->B, B_fill_number);

    pthread_mutex_unlock(&console_mutex);

    // Усі дані введено. Один учасник фіксує початок часу.
    int barrier_status = pthread_barrier_wait(&input_ready);
    if (barrier_status != 0 && barrier_status != PTHREAD_BARRIER_SERIAL_THREAD) {
        fprintf(stderr, "Input barrier error: %d\n", barrier_status);
        exit(EXIT_FAILURE);
    }
    if (barrier_status == PTHREAD_BARRIER_SERIAL_THREAD) {
        if (clock_gettime(CLOCK_MONOTONIC, &start_time) != 0) {
            perror("clock_gettime");
            exit(EXIT_FAILURE);
        }
    }
    // Не починати обчислення, доки start_time не записано.
    pthread_barrier_wait(&input_ready);

    int start = sm->N / 4;
    int end = sm->N / 2;

    for (int j = start; j < end; j++) {
        long long sum = 0;

        for (int i = 0; i < sm->N; i++) {
            sum += sm->B.data[i]
                 * sm->MR.data[(size_t)i * sm->N + j];
        }

        sm->V.data[j] = sum;
    }

    for (int j = start; j < end; j++) {

        for (int i = 0; i < sm->N; i++) {

            long long sum = 0;

            for (int k = 0; k < sm->N; k++) {

                sum += sm->MM.data[(size_t)i * sm->N + k]
                     * sm->MO.data[(size_t)k * sm->N + j];

            }

            sm->MX.data[(size_t)i * sm->N + j] = sum;
        }

    }

    for (int i = start; i < end; i++) {
        if (sm->B.data[i] < local_min)
            local_min = sm->B.data[i];
    }

    long long current = atomic_load(&min_b);

    while (local_min < current) {
        if (atomic_compare_exchange_weak(
                &min_b, &current, local_min)) {
            break;
        }
    }

    pthread_barrier_wait(&intermediate_ready);

    long long minimum = atomic_load(&min_b);

    for (int j = start; j < end; j++) {

        long long sum = 0;

        for (int k = 0; k < sm->N; k++) {

            sum += sm->V.data[k] * sm->MX.data[(size_t)k * sm->N + j];

        }

        sm->E.data[j] = sum + minimum * sm->Q.data[j] * sm->d;

    }

    if (sem_post(&finished) == -1) {
        perror("sem_post");
        exit(EXIT_FAILURE);
    }

    return NULL;

}

void* F3(void* _) {

    shared_memory* sm = _;
    long long MO_fill_number, d;
    long long local_min = LLONG_MAX;

    pthread_mutex_lock(&console_mutex);

    printf("Input element for MO matrix: ");
    fflush(stdout);
    if (scanf("%lld", &MO_fill_number) != 1) {
        fprintf(stderr, "Invalid input for MO_fill_number\n");
        exit(EXIT_FAILURE);
    }

    value_fill_matrix(&sm->MO, MO_fill_number);

    printf("Input number for d: ");
    fflush(stdout);
    if (scanf("%lld", &d) != 1) {
        fprintf(stderr, "Invalid input for d\n");
        exit(EXIT_FAILURE);
    }

    sm->d = d;

    pthread_mutex_unlock(&console_mutex);

    // Усі дані введено. Один учасник фіксує початок часу.
    int barrier_status = pthread_barrier_wait(&input_ready);
    if (barrier_status != 0 && barrier_status != PTHREAD_BARRIER_SERIAL_THREAD) {
        fprintf(stderr, "Input barrier error: %d\n", barrier_status);
        exit(EXIT_FAILURE);
    }
    if (barrier_status == PTHREAD_BARRIER_SERIAL_THREAD) {
        if (clock_gettime(CLOCK_MONOTONIC, &start_time) != 0) {
            perror("clock_gettime");
            exit(EXIT_FAILURE);
        }
    }
    // Не починати обчислення, доки start_time не записано.
    pthread_barrier_wait(&input_ready);

    int start = sm->N / 2;
    int end = (int)(3LL * sm->N / 4);

    for (int j = start; j < end; j++) {
        long long sum = 0;

        for (int i = 0; i < sm->N; i++) {
            sum += sm->B.data[i]
                 * sm->MR.data[(size_t)i * sm->N + j];
        }

        sm->V.data[j] = sum;
    }

    for (int j = start; j < end; j++) {

        for (int i = 0; i < sm->N; i++) {

            long long sum = 0;

            for (int k = 0; k < sm->N; k++) {

                sum += sm->MM.data[(size_t)i * sm->N + k]
                     * sm->MO.data[(size_t)k * sm->N + j];

            }

            sm->MX.data[(size_t)i * sm->N + j] = sum;
        }

    }

    for (int i = start; i < end; i++) {
        if (sm->B.data[i] < local_min)
            local_min = sm->B.data[i];
    }

    long long current = atomic_load(&min_b);

    while (local_min < current) {
        if (atomic_compare_exchange_weak(
                &min_b, &current, local_min)) {
            break;
        }
    }

    pthread_barrier_wait(&intermediate_ready);

    long long minimum = atomic_load(&min_b);

    for (int j = start; j < end; j++) {

        long long sum = 0;

        for (int k = 0; k < sm->N; k++) {

            sum += sm->V.data[k] * sm->MX.data[(size_t)k * sm->N + j];

        }

        sm->E.data[j] = sum + minimum * sm->Q.data[j] * sm->d;

    }

    if (sem_post(&finished) == -1) {
        perror("sem_post");
        exit(EXIT_FAILURE);
    }

    return NULL;
}

void* F4(void* _) {

    shared_memory* sm = _;
    long long local_min = LLONG_MAX;

    // Усі дані введено. Один учасник фіксує початок часу.
    int barrier_status = pthread_barrier_wait(&input_ready);
    if (barrier_status != 0 && barrier_status != PTHREAD_BARRIER_SERIAL_THREAD) {
        fprintf(stderr, "Input barrier error: %d\n", barrier_status);
        exit(EXIT_FAILURE);
    }
    if (barrier_status == PTHREAD_BARRIER_SERIAL_THREAD) {
        if (clock_gettime(CLOCK_MONOTONIC, &start_time) != 0) {
            perror("clock_gettime");
            exit(EXIT_FAILURE);
        }
    }
    // Не починати обчислення, доки start_time не записано.
    pthread_barrier_wait(&input_ready);

    int start = (int)(3LL * sm->N / 4);
    int end = sm->N;

    for (int j = start; j < end; j++) {
        long long sum = 0;

        for (int i = 0; i < sm->N; i++) {
            sum += sm->B.data[i]
                 * sm->MR.data[(size_t)i * sm->N + j];
        }

        sm->V.data[j] = sum;
    }

    for (int j = start; j < end; j++) {

        for (int i = 0; i < sm->N; i++) {

            long long sum = 0;

            for (int k = 0; k < sm->N; k++) {

                sum += sm->MM.data[(size_t)i * sm->N + k]
                     * sm->MO.data[(size_t)k * sm->N + j];

            }

            sm->MX.data[(size_t)i * sm->N + j] = sum;
        }

    }

    for (int i = start; i < end; i++) {
        if (sm->B.data[i] < local_min)
            local_min = sm->B.data[i];
    }

    long long current = atomic_load(&min_b);

    while (local_min < current) {
        if (atomic_compare_exchange_weak(
                &min_b, &current, local_min)) {
            break;
        }
    }

    pthread_barrier_wait(&intermediate_ready);

    long long minimum = atomic_load(&min_b);

    for (int j = start; j < end; j++) {

        long long sum = 0;

        for (int k = 0; k < sm->N; k++) {

            sum += sm->V.data[k] * sm->MX.data[(size_t)k * sm->N + j];

        }

        sm->E.data[j] = sum + minimum * sm->Q.data[j] * sm->d;

    }

    if (sem_post(&finished) == -1) {
        perror("sem_post");
        exit(EXIT_FAILURE);
    }

    return NULL;
}

int main(void) {

    shared_memory sm = {0};
    pthread_t T1, T2, T3, T4;
    int N;

    printf("Enter N number: ");
    fflush(stdout);
    if (scanf("%d", &N) != 1 || N <= 0) {
        fprintf(stderr, "N must be a positive integer\n");
        return EXIT_FAILURE;
    }

    sm.N = N;
    sm.B = init_vector(N);
    sm.Q = init_vector(N);
    sm.E = init_vector(N);
    sm.V = init_vector(N);
    sm.MR = init_matrix(N);
    sm.MM = init_matrix(N);
    sm.MO = init_matrix(N);
    sm.MX = init_matrix(N);

    int result = EXIT_FAILURE;
    if (!sm.B.data || !sm.Q.data || !sm.E.data || !sm.V.data ||
        !sm.MR.data || !sm.MM.data || !sm.MO.data || !sm.MX.data) {
        fprintf(stderr, "Memory allocation error\n");
        goto free_memory;
    }

    int status = pthread_barrier_init(&input_ready, NULL, 4);
    if (status != 0) {
        fprintf(stderr, "Input barrier init error: %d\n", status);
        goto free_memory;
    }
    status = pthread_barrier_init(&intermediate_ready, NULL, 4);
    if (status != 0) {
        fprintf(stderr, "Intermediate barrier init error: %d\n", status);
        pthread_barrier_destroy(&input_ready);
        goto free_memory;
    }
    atomic_init(&min_b, LLONG_MAX);
    if (sem_init(&finished, 0, 0) == -1) {
        perror("sem_init");
        pthread_barrier_destroy(&input_ready);
        pthread_barrier_destroy(&intermediate_ready);
        goto free_memory;
    }

    const int t1_status = pthread_create(&T1, NULL, F1, &sm);
    const int t2_status = pthread_create(&T2, NULL, F2, &sm);
    const int t3_status = pthread_create(&T3, NULL, F3, &sm);
    const int t4_status = pthread_create(&T4, NULL, F4, &sm);

    // Перевірка до join: відсутній потік не дійде до бар'єра.
    if (t1_status != 0 || t2_status != 0 || t3_status != 0 || t4_status != 0) {
        fprintf(stderr, "Thread creation error: T1=%d, T2=%d, T3=%d, T4=%d\n",
                t1_status, t2_status, t3_status, t4_status);
        exit(EXIT_FAILURE);
    }

    const int j1 = pthread_join(T1, NULL);
    const int j2 = pthread_join(T2, NULL);
    const int j3 = pthread_join(T3, NULL);
    const int j4 = pthread_join(T4, NULL);
    if (j1 != 0 || j2 != 0 || j3 != 0 || j4 != 0) {
        fprintf(stderr, "Thread join error: %d, %d, %d, %d\n", j1, j2, j3, j4);
        exit(EXIT_FAILURE);
    }

    const double elapsed_seconds =
        (double)(end_time.tv_sec - start_time.tv_sec) +
        (double)(end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;
    printf("Completed\n");
    printf("Threads computation time: %.6f seconds\n", elapsed_seconds);

    sem_destroy(&finished);
    pthread_barrier_destroy(&input_ready);
    pthread_barrier_destroy(&intermediate_ready);
    result = EXIT_SUCCESS;

free_memory:
    pthread_mutex_destroy(&console_mutex);
    free_vector(&sm.B);
    free_vector(&sm.Q);
    free_vector(&sm.E);
    free_vector(&sm.V);
    free_matrix(&sm.MR);
    free_matrix(&sm.MM);
    free_matrix(&sm.MO);
    free_matrix(&sm.MX);
    return result;
}
