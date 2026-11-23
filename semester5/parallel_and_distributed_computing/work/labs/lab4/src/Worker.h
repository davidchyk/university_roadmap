#ifndef LAB4_WORKER_H
#define LAB4_WORKER_H

#include "Data.h"

class Worker {
protected:
    static void calculate(int tid) {
        const int first = Data::begin(tid);
        const int last = Data::end(tid);

        Data::calculateIntermediateColumns(first, last);
        const Data::value_t partial = Data::localDot(first, last);

#pragma omp atomic update
        Data::s += partial;

#pragma omp barrier

        Data::value_t localS;
        Data::value_t localD;
        Data::value_t localP;

        omp_set_lock(&Data::lockS);
        localS = Data::s;
        omp_unset_lock(&Data::lockS);

#pragma omp critical(CS_d)
        { localD = Data::d; }

#pragma omp critical(CS_p)
        { localP = Data::p; }

        Data::calculateResultColumns(first, last, localS, localD, localP);
    }
};

#endif
