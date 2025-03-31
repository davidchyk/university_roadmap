import numpy as np # Задля обробки масивів даних
from tabulate import tabulate # Задля красивоговиводу таблиці
import math # Задля кореня та натурального логарифму

STUDENT_COEF = 1.73 # Коефіцієнт Стьюдента
T_u = 0.452 # Обчислена похибка вирмірювання напруги на екрані осцилографа
Delta_A = [] # Список абсолютних похибок вимірювання амплітуди для всіх значень опору R_m
relative_A = [] # Список відносних похибок вимірювання амплітуди для всіх значень опору R_m

# Виміряні значення 3 амплітуд для різних значень опору R_m (змінюється з кожним рядком)
A_data = np.array([

    [5.4547, 4.5516, 3.8292],
    [4.8769, 3.6485, 2.7093],
    [4.3710, 2.8899, 1.8785],
    [3.9014, 2.2758, 1.3366],
    [3.4679, 1.8423, 0.9392],
    [3.0706, 1.4450, 0.6864]

])

#============================T=============================== Обчислення похибки для T

mean_l1 = 4e-3 # l1, с
mean_l = 0.4e-3 # l, с
mean_nu = 250 # частота, Гц

S_l1 = 12e-5 # Обчислена абсолютна похибка для l1
S_l = 12e-6 # Обчислена абсолютна похибка для l

S_nu = 0.25 # Обчислена абсолютна похибка для частоти

# Обчислення абсолютної похибки для T
Delta_T = math.sqrt(

    ((mean_l * S_l1) / (mean_l1**2 * mean_nu))**2 +
    (S_l / (mean_l1 * mean_nu))**2 +
    ((mean_l * S_nu) / (mean_l1 * mean_nu**2))**2

)

# Обчислення відносної похибки для T
Epsilon_T = math.sqrt(

    ((S_l1 / mean_l1)**2) +
    ((S_l / mean_l)**2) +
    ((S_nu / mean_nu)**2)

)
Epsilon_T = round(Epsilon_T, 4) * 100 # Округлюємо та переводимо у відсотки

print(f"\nDelta_T = {Delta_T} с")
print(f"Epsilon_T = {Epsilon_T} %")

#============================A=============================== Обчислення похибки для A

Delta_A = np.sqrt((A_data * 0.03)**2 + T_u**2) # Створення масиву абсолютних похибок

# Знаходження середніх значень для всього масиву, та для 1 та 3 стовпців
Delta_A_mean = np.mean(Delta_A) 
Delta_A1_mean = np.mean(Delta_A[:, 0])
Delta_A3_mean = np.mean(Delta_A[:, 1])

# Обчислення загальної абсолютної та відносної похибок для A
Delta_A_VALUE = np.sqrt(np.sum((Delta_A - Delta_A_mean)**2) / (len(Delta_A) * (len(Delta_A) - 1))) * STUDENT_COEF
Delta_A_VALUE = round(Delta_A_VALUE, 4)
ALL_relative_A = round(Delta_A_VALUE / Delta_A_mean * 100, 4)

# Окреме обчислення похибок для стовпців 1 та 3
S_A_i1 = np.sqrt(np.sum((Delta_A[:, 0] - Delta_A1_mean)**2) / (len(Delta_A[:, 0]) * (len(Delta_A[:, 0]) - 1)))
S_A_i1 = round(S_A_i1, 4)

S_A_i3 = np.sqrt(np.sum((Delta_A[:, 2] - Delta_A3_mean)**2) / (len(Delta_A[:, 2]) * (len(Delta_A[:, 2]) - 1)))
S_A_i3 = round(S_A_i3, 4)

# Вивід результатів обрахунків
print(f"\nDelta_A = {Delta_A_VALUE} В")
print(f"epsilon_A = {ALL_relative_A} %")

print(f"\nS_A_i = {S_A_i1} В")
print(f"S_A_i+2 = {S_A_i3} В")

#============================lambda=============================== Обчислення похибки для lambda

mean_A_i1 = 4.1904 # Середнє значення ампліуд напруг для стовпця 1
mean_A_i3 = 1.8965 # Середнє значення ампліуд напруг для стовпця 3

# Обчислення абсолютної похибки для lambda
Delta_lambda = math.sqrt(((2 * S_A_i1) / 3 * mean_A_i1)**2 + ((2 * S_A_i3) / 3 * mean_A_i3)**2)
Delta_lambda = round(Delta_lambda, 4)

# Обчислення відносної похибки для lambda
Epsilon_lambda = math.sqrt(S_A_i1**2 + S_A_i3**2) / (math.log(mean_A_i1) - math.log(mean_A_i3))
Epsilon_lambda = round(Epsilon_lambda, 4) * 100

# Вивід результатів обрахунків
print(f"\nDelta_lambda = {Delta_lambda}")
print(f"Epsilon_lambda = {Epsilon_lambda} %")

#============================beta================================= Обчислення похибки для beta

mean_lambda = 0.6039 # Середнє значення lambda
mean_T = 0.4e-3 # Середнє значення T

S_lambda = Delta_lambda # Обчислена абсолютна похибка для lambda
S_T = Delta_T # Обчислена абсолютна похибка для T

# Обчислення абсолютної похибки для beta
Delta_beta = 1 / mean_T**2 * math.sqrt(

    (mean_T * S_lambda)**2 +
    (mean_l * S_T)**2

)
Delta_beta = round(Delta_beta, 4)

# Обчислення відносної похибки для beta
Epsilon_beta = math.sqrt(

    (S_lambda / mean_lambda)**2 +
    (S_T / mean_T)**2

)
Epsilon_beta = round(Epsilon_beta, 4) * 100

print(f"\nDelta_beta = {Delta_beta} c^{-1}")
print(f"Epsilon_beta = {Epsilon_beta} %")

#============================R================================= Обчислення похибки для R

mean_R_m = 350 # Середнє значення опору R_m
mean_r_k = 63.0058 # Середнє значення опору r_k

S_R_m = 17.5 # Обчислена абсолютна похибка для R_m
S_r_k = 3.15 # Обчислена абсолютна похибка для r_k

# Обчислення абсолютної похибки для R
Delta_R = math.sqrt(S_R_m**2 + S_r_k**2)
Delta_R = round(Delta_R, 4)

# Обчислення відносної похибки для R
Epsilon_R = math.sqrt(

    (S_R_m / mean_R_m)**2 + 
    (S_r_k / mean_r_k)**2

)
Epsilon_R = round(Epsilon_R, 4) * 100

# Вивід результатів обрахунків
print(f"\nDelta_R = {Delta_R} Ом")
print(f"Epsilon_R = {Epsilon_R} %")

#============================L================================= Обчислення похибки для L

mean_R = 350 # Середнє значення опору R
mean_lambda = 0.6039 # Середнє значення lambda
mean_T = 0.4e-3 # Середнє значення T

S_R = 17.7812 # Обчислена абсолютна похибка для R
S_lambda = 0.0091 # Обчислена абсолютна похибка для lambda
S_T = 1.69e-5 # Обчислена абсолютна похибка для T

# Обчислення абсолютної похибки для L
Delta_L = math.sqrt(

    ((mean_T * S_R) / (2 * mean_lambda))**2 +
    ((mean_R * mean_T * S_lambda) / (2 * mean_lambda**2))**2 +
    (mean_R * S_T / (2 * mean_lambda))**2

)
Delta_L = round(Delta_L, 4)

# Обчислення відносної похибки для L
Epsilon_L = math.sqrt(

    (S_R / mean_R)**2 +
    (S_lambda / mean_lambda)**2 +
    (S_T / mean_T)**2

) * 100
Epsilon_L = round(Epsilon_L, 4)

# Вивід результатів обрахунків
print(f"\nDelta_L = {Delta_L} Гн")
print(f"Epsilon_L = {Epsilon_L} %")

#============================C================================= Обчислення похибки для C

mean_L = 0.1322 # Середнє значення L
mean_T = 0.4e-3 # Середнє значення T

S_L = 0.0079 # Обчислена абсолютна похибка для L
S_T = 1.69e-5 # Обчислена абсолютна похибка для T

# Обчислення абсолютної похибки для C
Delta_C = math.sqrt(

    (((mean_T / (2 * math.pi * mean_L))**2 * S_L))**2 +
    ((S_T * mean_T) / (2 * math.pi**2 * mean_L))**2

) * 1e6 # Для заміни з Ф, на мкФ
Delta_C = round(Delta_C, 4)

# Обчислення відносної похибки для C
Epsilon_C = math.sqrt(

    (S_L / mean_L)**2 +
    (S_T / mean_T)**2

) * 100
Epsilon_C = round(Epsilon_C, 4)

# Вивід результатів обрахунків
print(f"\nDelta_C = {Delta_C} мкФ")
print(f"Epsilon_C = {Epsilon_C} %")

#============================R cr=================================

mean_C = 0.0306e-6 # Середнє значення C
mean_L = 0.1322 # Середнє значення L

S_C = 0.0032e-6 # Обчислена абсолютна похибка для C
S_L = 0.0079 # Обчислена абсолютна похибка для L

# Обчислення абсолютної похибки для R cr
Delta_R_cr = math.sqrt(

    ((mean_L * S_C**2) / mean_C**3) +
    (S_L**2 / (mean_C * mean_L))

)
Delta_R_cr = round(Delta_R_cr, 4)

# Обчислення відносної похибки для R cr
Epsilon_R_cr = math.sqrt(

    (S_C / (2 * mean_C))**2 +
    (S_L / (2 * mean_L))**2

) * 100
Epsilon_R_cr = round(Epsilon_R_cr, 4)

# Вивід результатів обрахунків
print(f"\nDelta_R_cr = {Delta_R_cr} Ом")
print(f"Epsilon_R_cr = {Epsilon_R_cr} %")