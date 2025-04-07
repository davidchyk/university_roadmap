import numpy as np # Для роботи з масивами даних
import math # Для арифметичого квадратного кореня, та числа пі

R1 = 100 # Опір резистора R1, Ом

# Вектор значення змінюваної частоти, кГц
Frequency_vector = np.array([1, 2, 3, 4, 5, 6, 7, 7.7, 7.9, 8.1, 9, 10, 11, 12, 13, 14, 15, 16])

# Значення виміряних позначок A, поділка. Де кожен рядок, це значення при певному значенні опору R.
A_matrix = np.array([

    [0.27, 0.24, 0.24, 0.24, 0.24, 0.24, 0.69, 2.37, 1.04, 0.21, 0.24, 0.24, 0.24, 0.24, 0.23, 0.24, 0.24],
    [0.25, 0.24, 0.24, 0.27, 0.44, 1.00, 2.37, 2.90, 2.66, 0.98, 0.56, 0.39, 0.29, 0.24, 0.24, 0.26, 0.24],
    [0.24, 0.24, 0.33, 0.45, 0.64, 0.89, 1.02, 1.02, 1.00, 0.89, 0.72, 0.57, 0.49, 0.41, 0.37, 0.33, 0.30]

])

# Вектор значення змінюваної ємності C, нФ
С_matrix = np.array([1, 2, 3, 4, 5, 6, 7, 7.7, 7.9, 8.1, 9, 10])

# Вектор виставлених значень опорів резистора R, Ом
R_vector = np.array([1, 500, 3000])

# Вектор значення резонансних частот, кГц
RESONANS_frequency_vector = np.array([13.757, 9.728, 7.943, 6.879, 6.152, 5.616, 5.200, 4.864, 4.586, 4.350])

# Обчислення абсолютної похибки вимірювання частот
Absolute_mistakeFrequency_vector = Frequency_vector * 0.01
ABS_mean_Frequency = np.round(np.mean(Absolute_mistakeFrequency_vector) * 1000, 2)
print(f"Delta f = {ABS_mean_Frequency} Гц")

# Обчислення абсолютної похибки вимірювання значень поділок амплітуд
Absolute_mistakeA_matrix = A_matrix * 0.02
ABS_mean_A = np.round(np.mean(Absolute_mistakeA_matrix), 2)
print(f"Delta A = {ABS_mean_A} поділок")

# Обчислення абсолютної похибки вимірювання значень ємностей контуру
Absolute_mistakeC_matrix = С_matrix * 0.05
ABS_mean_C = np.round(np.mean(Absolute_mistakeC_matrix), 2)
print(f"Delta C = {ABS_mean_C} нФ")

# Обчислення абсолютної похибки вимірювання опору резистора R1
Absolute_mistakeR1 = R1 * 0.01
print(f"Delta R1 = {Absolute_mistakeR1} Ом")

# Обчислення абсолютної похибки вимірювання значень опору резистора R
Absolute_mistakeR_vector = R_vector * 0.04
ABS_mean_R = np.mean(Absolute_mistakeR_vector)
print(f"Delta R = {ABS_mean_R} Ом")

# Обчислення абсолютної похибки вимірювання сили струму I0
Absolute_mistakeI0 = math.sqrt(

    (ABS_mean_A / R1)**2 +
    (np.mean(A_matrix) * Absolute_mistakeR1 / R1**2)**2

) * 1000 # для переводу з А в мА

# Обчислення відносної похибки вимірювання сили струму I0
Relivate_mistakeI0 = math.sqrt(

    (ABS_mean_A / np.mean(A_matrix))**2 +
    (Absolute_mistakeR1 / R1)**2

) * 100 # для відсоткового представлення

# Вивід результатів обрахунків
print(f"Delta I0 = {round(Absolute_mistakeI0, 2)}, мА")
print(f"Epsilon I0 = {round(Relivate_mistakeI0, 2)} %")

# Обчислення абсолютної похибки вимірювання часової харакети Z
MEAN_RESONANS_frequency_vector = np.mean(RESONANS_frequency_vector) * 1000

Absolute_mistakeZ = round(ABS_mean_Frequency / (2 * math.pi * MEAN_RESONANS_frequency_vector**3) * 1e10, 2)
Relivate_mistakeZ = round(2 / (MEAN_RESONANS_frequency_vector) * 100, 2)

# Вивід результатів обрахунків
print(f"Delta Z = {Absolute_mistakeZ} * 10^-10 с^2")
print(f"Epsilon Z = {Relivate_mistakeZ} %")