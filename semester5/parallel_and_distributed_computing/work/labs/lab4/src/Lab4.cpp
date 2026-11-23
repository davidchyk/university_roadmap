/*
 * Дисципліна: Паралельні та розподілені обчислення
 * Лабораторна робота №4: OpenMP. Бар'єри, критичні секції
 * Варіант 7
 * MA = (MR * MC) * d + (B * Z) * (MZ * MM) * p
 * T1: MC, B; T2: Z, d, p; T3: MA, MM; T4: MR, MZ
 * Виконав: студент групи ІО-41 Давидчук Артем Миколайович
 */

#include "Data.h"
#include "T1.h"
#include "T2.h"
#include "T3.h"
#include "T4.h"

#include <cstdlib>
#include <exception>
#include <iomanip>
#include <iostream>
#include <omp.h>

int main(int argc, char** argv) {
    try {
        const int n = argc > 1 ? std::stoi(argv[1]) : 4;
        Data::init(n);
        omp_set_dynamic(0);

        T1 t1;
        T2 t2;
        T3 t3;
        T4 t4;

        const double start = omp_get_wtime();

#pragma omp parallel num_threads(Data::P) shared(t1, t2, t3, t4)
        {
            switch (omp_get_thread_num()) {
                case 0: t1.run(0); break;
                case 1: t2.run(1); break;
                case 2: t3.run(2); break;
                case 3: t4.run(3); break;
            }
        }

        const double elapsed = omp_get_wtime() - start;
        std::cout << std::fixed << std::setprecision(6)
                  << "Computation time: " << elapsed << " seconds\n";

        Data::cleanup();
        return EXIT_SUCCESS;
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        return EXIT_FAILURE;
    }
}
