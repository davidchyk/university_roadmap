import numpy as np
import math
from tabulate import tabulate

# Вектор кутів падіння у радіанах (переведення з градусів у радіани)
teta_vector = np.deg2rad(np.array([10, 20, 30, 40, 50, 60, 70, 80]))

# Початкове значення напруги для перпендикулярної компоненти
U0_perp = 276.85
# Вектор експериментальних значень напруги для перпендикулярної компоненти
U_perp_vector = np.array([25.28, 28.43, 32.88, 41.44, 55.16, 78.00, 155.61, 176.97])

# Початкове значення напруги для паралельної компоненти
U0_paral = 238.72
# Вектор експериментальних значень напруги для паралельної компоненти
U_paral_vector = np.array([20.42, 18.28, 14.77, 9.85, 4.17, 0.12, 5.63, 48.39])

# Обчислення для перпендикулярної компоненти
# Квадратний корінь з експериментальних значень напруги
sqrt_U_perp_vector = np.round(np.sqrt(U_perp_vector), 4)
# Експериментальне відношення амплітуд E_perp/E0
Eperp_E0_expr = np.round(sqrt_U_perp_vector / math.sqrt(U0_perp), 4)

# Теоретичне відношення амплітуд E_perp/E0 за формулами Френеля
k = 2/3  # Відношення показників заломлення n1/n2
Eperp_E0_theor = np.round(
    np.sin(teta_vector - np.arcsin(k * np.sin(teta_vector))) /
    np.sin(teta_vector + np.arcsin(k * np.sin(teta_vector))), 4
)

# Обчислення для паралельної компоненти
# Квадратний корінь з експериментальних значень напруги
sqrt_U_paral_vector = np.round(np.sqrt(U_paral_vector), 4)
# Експериментальне відношення амплітуд E_paral/E0
Eparal_E0_expr = np.round(sqrt_U_paral_vector / math.sqrt(U0_paral), 4)

# Теоретичне відношення амплітуд E_paral/E0 за формулами Френеля
Eparal_E0_theor = np.round(
    np.tan(teta_vector - np.arcsin(k * np.sin(teta_vector))) /
    np.tan(teta_vector + np.arcsin(k * np.sin(teta_vector))), 4
)

# Формування горизонтальної таблиці для виводу результатів
table_data = [
    ["U_perp"] + list(U_perp_vector),  # Експериментальні значення U_perp
    ["sqrt(U_perp)"] + list(sqrt_U_perp_vector),  # Квадратний корінь з U_perp
    ["E_perp/E0 EXPERIMENTAL"] + list(Eperp_E0_expr),  # Експериментальне E_perp/E0
    ["E_perp/E0 THEORETICAL"] + list(Eperp_E0_theor),  # Теоретичне E_perp/E0
    ["U_paral"] + list(U_paral_vector),  # Експериментальні значення U_paral
    ["sqrt(U_paral)"] + list(sqrt_U_paral_vector),  # Квадратний корінь з U_paral
    ["E_paral/E0 EXPERIMENTAL"] + list(Eparal_E0_expr),  # Експериментальне E_paral/E0
    ["E_paral/E0 THEORETICAL"] + list(Eparal_E0_theor),  # Теоретичне E_paral/E0
]

# Вивід таблиці у форматі "fancy_grid"
print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))

# Додатковий розрахунок: cos^2(alpha) для кутів від 0 до 85 градусів з кроком 5
angle_vector = np.deg2rad(np.arange(0, 86, 5))  # Кути у радіанах
cos_vector = np.round(np.square(np.cos(angle_vector)), 2)  # cos^2(alpha)

# Вивід таблиці для cos^2(alpha)
print(tabulate([["alpha"] + list(np.arange(0, 86, 5)), ["cos^2 alpha"] + list(cos_vector)], headers="firstrow", tablefmt="fancy_grid"))