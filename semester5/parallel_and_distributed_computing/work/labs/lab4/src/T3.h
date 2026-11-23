#ifndef LAB4_T3_H
#define LAB4_T3_H

#include "Worker.h"

#include <algorithm>
#include <iostream>

class T3 final : private Worker {
public:
    void run(int tid) const {
        Data::fillMatrix(Data::MM, 1);
#pragma omp barrier
        calculate(tid);
#pragma omp barrier

        const int shown = std::min(Data::N, 10);
        std::cout << "First row of MA: ";
        for (int j = 0; j < shown; ++j) {
            std::cout << Data::MA[j] << (j + 1 == shown ? "" : " ");
        }
        if (Data::N > shown) std::cout << " ...";
        std::cout << "\nChecksum: " << Data::checksum() << '\n';
    }
};

#endif
