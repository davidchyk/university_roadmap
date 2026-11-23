#include "Data.h"

#include <algorithm>
#include <numeric>
#include <stdexcept>

int Data::N = 0;
std::vector<Data::value_t> Data::B, Data::Z;
std::vector<Data::value_t> Data::MC, Data::MM, Data::MR, Data::MZ;
std::vector<Data::value_t> Data::X, Data::Y, Data::MA;
Data::value_t Data::d = 0;
Data::value_t Data::p = 0;
Data::value_t Data::s = 0;
omp_lock_t Data::lockS;

void Data::init(int n) {
    if (n <= 0) {
        throw std::invalid_argument("N must be positive");
    }
    N = n;
    const std::size_t matrixSize = static_cast<std::size_t>(N) * N;
    B.assign(N, 0);
    Z.assign(N, 0);
    MC.assign(matrixSize, 0);
    MM.assign(matrixSize, 0);
    MR.assign(matrixSize, 0);
    MZ.assign(matrixSize, 0);
    X.assign(matrixSize, 0);
    Y.assign(matrixSize, 0);
    MA.assign(matrixSize, 0);
    d = p = s = 0;
    omp_init_lock(&lockS);
}

void Data::cleanup() { omp_destroy_lock(&lockS); }

void Data::fillVector(std::vector<value_t>& v, value_t value) {
    std::fill(v.begin(), v.end(), value);
}

void Data::fillMatrix(std::vector<value_t>& m, value_t value) {
    std::fill(m.begin(), m.end(), value);
}

int Data::begin(int tid) { return tid * N / P; }
int Data::end(int tid) { return (tid + 1) * N / P; }

Data::value_t Data::localDot(int first, int last) {
    value_t result = 0;
    for (int i = first; i < last; ++i) {
        result += B[i] * Z[i];
    }
    return result;
}

void Data::calculateIntermediateColumns(int firstColumn, int lastColumn) {
    for (int i = 0; i < N; ++i) {
        const std::size_t row = static_cast<std::size_t>(i) * N;
        for (int j = firstColumn; j < lastColumn; ++j) {
            value_t x = 0;
            value_t y = 0;
            for (int k = 0; k < N; ++k) {
                x += MR[row + k] * MC[static_cast<std::size_t>(k) * N + j];
                y += MZ[row + k] * MM[static_cast<std::size_t>(k) * N + j];
            }
            X[row + j] = x;
            Y[row + j] = y;
        }
    }
}

void Data::calculateResultColumns(int firstColumn, int lastColumn,
                                  value_t localS, value_t localD,
                                  value_t localP) {
    for (int i = 0; i < N; ++i) {
        const std::size_t row = static_cast<std::size_t>(i) * N;
        for (int j = firstColumn; j < lastColumn; ++j) {
            MA[row + j] = X[row + j] * localD
                        + Y[row + j] * localS * localP;
        }
    }
}

Data::value_t Data::checksum() {
    return std::accumulate(MA.begin(), MA.end(), value_t{0});
}
