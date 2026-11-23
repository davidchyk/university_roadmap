#ifndef LAB4_DATA_H
#define LAB4_DATA_H

#include <cstdint>
#include <vector>
#include <omp.h>

class Data {
public:
    using value_t = std::int64_t;
    static constexpr int P = 4;

    static int N;
    static std::vector<value_t> B, Z;
    static std::vector<value_t> MC, MM, MR, MZ;
    static std::vector<value_t> X, Y, MA;
    static value_t d, p, s;
    static omp_lock_t lockS;

    static void init(int n);
    static void cleanup();
    static void fillVector(std::vector<value_t>& v, value_t value);
    static void fillMatrix(std::vector<value_t>& m, value_t value);
    static int begin(int tid);
    static int end(int tid);
    static value_t localDot(int first, int last);
    static void calculateIntermediateColumns(int firstColumn, int lastColumn);
    static void calculateResultColumns(int firstColumn, int lastColumn,
                                       value_t localS, value_t localD,
                                       value_t localP);
    static value_t checksum();
};

#endif
