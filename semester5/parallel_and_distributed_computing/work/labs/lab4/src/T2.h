#ifndef LAB4_T2_H
#define LAB4_T2_H

#include "Worker.h"

class T2 final : private Worker {
public:
    void run(int tid) const {
        Data::fillVector(Data::Z, 1);
        Data::d = 1;
        Data::p = 1;
#pragma omp barrier
        calculate(tid);
#pragma omp barrier
    }
};

#endif
