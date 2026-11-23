#ifndef LAB4_T4_H
#define LAB4_T4_H

#include "Worker.h"

class T4 final : private Worker {
public:
    void run(int tid) const {
        Data::fillMatrix(Data::MR, 1);
        Data::fillMatrix(Data::MZ, 1);
#pragma omp barrier
        calculate(tid);
#pragma omp barrier
    }
};

#endif
