#ifndef LAB4_T1_H
#define LAB4_T1_H

#include "Worker.h"

class T1 final : private Worker {
public:
    void run(int tid) const {
        Data::fillMatrix(Data::MC, 1);
        Data::fillVector(Data::B, 1);
#pragma omp barrier
        calculate(tid);
#pragma omp barrier
    }
};

#endif
