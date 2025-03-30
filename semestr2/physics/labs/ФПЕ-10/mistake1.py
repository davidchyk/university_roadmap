import numpy as np # Задля обробки масивів даних
from tabulate import tabulate # Задля красивоговиводу таблиці
import math

STUDENT_COEF = 1.73
T_u = 0.452
Delta_A = []
relative_A = []

# Виміряні значення 3 амплітуд для різних значень опору R_m (змінюється з кожним рядком)
A_data = np.array([

    [5.4547, 4.5516, 3.8292],
    [4.8769, 3.6485, 2.7093],
    [4.3710, 2.8899, 1.8785],
    [3.9014, 2.2758, 1.3366],
    [3.4679, 1.8423, 0.9392],
    [3.0706, 1.4450, 0.6864]

])

#============================T===============================

mean_l1 = 0.4
mean_l = 4e-3
mean_nu = 250

S_l1 = S_l = 2e-4
S_nu = 0.25

Delta_T = math.sqrt(

    ((mean_l * S_l1) / (mean_l1**2 * mean_nu))**2 +
    (S_l / (mean_l1 * mean_nu))**2 +
    ((mean_l * S_nu) / (mean_l1 * mean_nu**2))**2

)

Epsilon_T = math.sqrt(

    ((S_l1 / mean_l1)**2) +
    ((S_l / mean_l)**2) +
    ((S_nu / mean_nu)**2)

)
Epsilon_T = round(Epsilon_T, 4) * 100

print(f"\nDelta_T = {Delta_T} с")
print(f"Epsilon_T = {Epsilon_T} %")

#============================A===============================

Delta_A = np.sqrt((A_data * 0.03)**2 + T_u**2)

Delta_A_mean = np.mean(Delta_A)
Delta_A1_mean = np.mean(Delta_A[:, 0])
Delta_A3_mean = np.mean(Delta_A[:, 1])

Delta_A_VALUE = np.sqrt(np.sum((Delta_A - Delta_A_mean)**2) / (len(Delta_A) * (len(Delta_A) - 1))) * STUDENT_COEF
Delta_A_VALUE = round(Delta_A_VALUE, 4)
ALL_relative_A = round(Delta_A_VALUE / Delta_A_mean * 100, 4)

S_A_i1 = np.sqrt(np.sum((Delta_A[:, 0] - Delta_A1_mean)**2) / (len(Delta_A[:, 0]) * (len(Delta_A[:, 0]) - 1)))
S_A_i1 = round(S_A_i1, 4)

S_A_i3 = np.sqrt(np.sum((Delta_A[:, 2] - Delta_A3_mean)**2) / (len(Delta_A[:, 2]) * (len(Delta_A[:, 2]) - 1)))
S_A_i3 = round(S_A_i3, 4)

print(f"\nDelta_A = {Delta_A_VALUE} В")
print(f"epsilon_A = {ALL_relative_A} %")

print(f"\nS_A_i = {S_A_i1} В")
print(f"S_A_i+2 = {S_A_i3} В")

#============================lambda===============================

mean_A_i1 = 4.1904
mean_A_i3 = 1.8965

Delta_lambda = math.sqrt(((2 * S_A_i1) / 3 * mean_A_i1)**2 + ((2 * S_A_i3) / 3 * mean_A_i3)**2)
Delta_lambda = round(Delta_lambda, 4)

Epsilon_lambda = math.sqrt(S_A_i1**2 + S_A_i3**2) / (math.log(mean_A_i1) - math.log(mean_A_i3))
Epsilon_lambda = round(Epsilon_lambda, 4) * 100

print(f"\nDelta_lambda = {Delta_lambda}")
print(f"Epsilon_lambda = {Epsilon_lambda} %")

#============================beta=================================

mean_lambda = 0.6039
mean_T = 0.4

S_lambda = Delta_lambda
S_T = Delta_T

Delta_beta = 1 / mean_T**2 * math.sqrt(

    (mean_T * S_lambda)**2 +
    (mean_l * S_T)**2

)
Delta_beta = round(Delta_beta, 4)

Epsilon_beta = math.sqrt(

    (S_lambda / mean_lambda)**2 +
    (S_T / mean_T)**2

)
Epsilon_beta = round(Epsilon_beta, 4) * 100

print(f"\nDelta_beta = {Delta_beta} c^{-1}")
print(f"Epsilon_beta = {Epsilon_beta} %")

#============================R=================================

mean_R_m = 350
mean_r_k = 63.0058

S_R_m = 17.5
S_r_k = 3.15

Delta_R = math.sqrt(S_R_m**2 + S_r_k**2)
Delta_R = round(Delta_R, 4)

Epsilon_R = math.sqrt(

    (S_R_m / mean_R_m)**2 + 
    (S_r_k / mean_r_k)**2

)
Epsilon_R = round(Epsilon_R, 4) * 100

print(f"\nDelta_R = {Delta_R} Ом")
print(f"Epsilon_R = {Epsilon_R} %")

#============================L=================================

mean_R = 350
mean_lambda = 0.6039
mean_T = 0.4

S_R = 17.7812
S_lambda = 0.0091
S_T = 2e-6

Delta_L = math.sqrt(

    ((mean_T * S_R) / (2 * mean_lambda))**2 +
    ((mean_R * S_lambda) / (2 * mean_lambda**2))**2 +
    (S_T / (2 * mean_lambda))**2

)
Delta_L = round(Delta_L, 4)

Epsilon_L = math.sqrt(

    (S_R / mean_R)**2 +
    (S_lambda / mean_lambda)**2 +
    (S_T / mean_T)**2

) * 100
Epsilon_L = round(Epsilon_L, 4)

print(f"\nDelta_L = {Delta_L} Гн")
print(f"Epsilon_L = {Epsilon_L} %")

#============================C=================================

mean_L = 132.2
mean_T = 0.4

S_L = 7.3311
S_T = 2e-6

Delta_C = math.sqrt(

    ((mean_T / (2 * math.pi * mean_L)**2 * S_L))**2 +
    ((S_T * mean_T) / (2 * math.pi * mean_L**2))**2

) * 1e6 # Для заміни з Ф, на мкФ
Delta_C = round(Delta_C, 4)

Epsilon_C = math.sqrt(

    (S_L / mean_L)**2 +
    (S_T / mean_T)**2

) * 100
Epsilon_C = round(Epsilon_C, 4)

print(f"\nDelta_C = {Delta_C} мкФ")
print(f"Epsilon_C = {Epsilon_C} %")

#============================R cr=================================

mean_C = 30.55 * 1e-6
mean_L = 132.2

S_C = 4.2502 * 1e-6
S_L = 7.3311

Delta_R_cr = math.sqrt(

    ((mean_L * S_C**2) / (mean_C**3))**2 +
    (S_L**2 / (mean_C * mean_L))**2

)
Delta_R_cr = round(Delta_R_cr, 4)

Epsilon_R_cr = math.sqrt(

    (S_C / (2 * mean_C))**2 +
    (S_L / (2 * mean_L))**2

) * 100
Epsilon_R_cr = round(Epsilon_R_cr, 4)

print(f"\nDelta_R_cr = {Delta_R_cr} Ом")
print(f"Epsilon_R_cr = {Epsilon_R_cr} %")