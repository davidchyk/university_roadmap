import numpy as np # Для роботи з масивами даних
from tabulate import tabulate # Для виводу таблиц

# Вектор значення змінюваної ємності C, нФ
C_vector = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Вектор значення резонансних частот, кГц
frequency_vector = np.array([13.757, 9.728, 7.943, 6.879, 6.152, 5.616, 5.200, 4.864, 4.586, 4.350])

# Вектор значення часової харакети Z, с^2 * 10^{-10}
Z_vector = 1 / (2 * np.pi * frequency_vector * 1000 )**2 * 1e10 # 1000 -- для переводу з кГц в Гц, 1e10 --- для переводу з 10^0 в 10^(-10)

# Знаходимо коефіцієнти лінійної регресії
k, b = np.polyfit(C_vector, Z_vector, 1)

# Створення таблиці: 3 рядки — C, Frequency, Z
table_data = [
    ["C, нФ"]      + [str(i) for i in range(1, 11)],
    ["f, кГц"]     + [f"{f:.3f}" for f in frequency_vector],
    ["Z, с^2 * 10^{-10}"]           + [f"{z:.3e}" for z in Z_vector]
]

# Вивід
print(tabulate(
    table_data,
    headers=[],
    tablefmt="fancy_grid"
))

# Вивід коефіцієнтів лінійної регресії: k та b
print(f"Z(C) ≈ {k:.3f}·C + {b:.3f}")