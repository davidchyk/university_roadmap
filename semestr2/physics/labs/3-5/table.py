import numpy as np
import math
from tabulate import tabulate

teta_vector = np.deg2rad(np.array([10, 20, 30, 40, 50, 60, 70, 80]))

U0_perp = 276.85
U_perp_vector = np.array([25.28, 28.43, 32.88, 41.44, 55.16, 78.00, 155.61, 176.97])

U0_paral = 238.72
U_paral_vector = np.array([20.42, 18.28, 14.77, 9.85, 4.17, 0.12, 5.63, 48.39])

# perp
sqrt_U_perp_vector = np.round(np.sqrt(U_perp_vector), 4)
Eperp_E0_expr = np.round(sqrt_U_perp_vector / math.sqrt(U0_perp), 4)

k = 2/3
Eperp_E0_theor = np.round(np.sin(teta_vector - np.arcsin(k * np.sin(teta_vector))) / np.sin(teta_vector + np.arcsin(k * np.sin(teta_vector))), 4)

#paral
sqrt_U_paral_vector = np.round(np.sqrt(U_paral_vector), 4)
Eparal_E0_expr = np.round(sqrt_U_paral_vector / math.sqrt(U0_paral), 4)

Eparal_E0_theor = np.round(np.tan(teta_vector - np.arcsin(k * np.sin(teta_vector))) / np.tan(teta_vector + np.arcsin(k * np.sin(teta_vector))), 4)

# Формуємо горизонтальну таблицю
table_data = [
    ["U_perp"] + list(U_perp_vector),
    ["sqrt(U_perp)"] + list(sqrt_U_perp_vector),
    ["E_perp/E0 EXPERIMENTAL"] + list(Eperp_E0_expr),
    ["E_perp/E0 THEORETICAL"] + list(Eperp_E0_theor),
    ["U_paral"] + list(U_paral_vector),
    ["sqrt(U_paral)"] + list(sqrt_U_paral_vector),
    ["E_paral/E0 EXPERIMENTAL"] + list(Eparal_E0_expr),
    ["E_paral/E0 THEORETICAL"] + list(Eparal_E0_theor),
]

# Виводимо таблицю
print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))

angle_vector = np.deg2rad(np.arange(0, 86, 5))
cos_vector = np.round(np.square(np.cos(angle_vector)), 2)

print(tabulate([["cos^2 alpha"] + list(cos_vector)], headers="firstrow", tablefmt="fancy_grid"))