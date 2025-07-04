import numpy as np # Для роботи з масивами даних
from tabulate import tabulate # Для виводу таблиці

Resistance_1 = 100 # Опір резистора R_1, Ом

# Значення виміряних позначок A, поділка. Де кожен рядок, це значення при певному значенні опору R.
A_matrix = np.array([

    [0.27, 0.24, 0.24, 0.24, 0.24, 0.24, 0.69, 2.37, 1.04, 0.21, 0.24, 0.24, 0.24, 0.24, 0.23, 0.24, 0.24],
    [0.25, 0.24, 0.24, 0.27, 0.44, 1.00, 2.37, 2.90, 2.66, 0.98, 0.56, 0.39, 0.29, 0.24, 0.24, 0.26, 0.24],
    [0.24, 0.24, 0.33, 0.45, 0.64, 0.89, 1.02, 1.02, 1.00, 0.89, 0.72, 0.57, 0.49, 0.41, 0.37, 0.33, 0.30]

])

# Зафіксовані значення коефіцієнтів підсилення K_y, В/поділку, відповідно до значень опору R.
K_y_matrix = np.array([

    [0.13, 0.22, 0.33, 0.52, 0.87, 1.94, 2.79, 2.79, 2.79, 1.97, 1.06, 0.75, 0.58, 0.48, 0.41, 0.36, 0.33],
    [0.13, 0.22, 0.33, 0.47, 0.47, 0.47, 0.47, 0.47, 0.47, 0.47, 0.47, 0.47, 0.47, 0.47, 0.41, 0.36, 0.32],
    [0.13, 0.21, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26]

])

# Вектор значення змінюваної частоти, кГц
frequency_vector = np.array([2, 3, 4, 5, 6, 7, 7.7, 7.9, 8.1, 9, 10, 11, 12, 13, 14, 15, 16])

# Обчислення значень сили струму I, мА, для всіх виміряних значень поділок амлпітуд.
Amperage0_matrix = A_matrix * K_y_matrix / Resistance_1 * 1000 # множимо на 1000, задля переводу з А в мА

# Підписи для рядків
row_headers = ["I0_1, мА", "I0_2, мА", "I0_3, мА"]

# Об’єднуємо заголовки з даними
table_data = [[row_headers[i]] + list(Amperage0_matrix[i]) for i in range(len(Amperage0_matrix))]

# Вивід таблиці
print(tabulate(
    table_data,
    headers=[r"I0 \ f, кГц"] + list(frequency_vector),
    tablefmt="fancy_grid",
    floatfmt=".2f"  # округлення до 2 знаків
))