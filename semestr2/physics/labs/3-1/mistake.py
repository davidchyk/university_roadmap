import numpy as np
import math

# Коефіцієнт Стьюдента для 6 вимірювань і довірчого рівня 90%
STUDENT_COEF = 2.02

# Таблиця виміряних значень x_i для червоного і зеленого світлофільтрів (у метрах)
X_table = np.array([
    [2.58e-3, 1.95e-3],  # Перше вимірювання
    [2.53e-3, 2.05e-3],  # Друге вимірювання
    [2.51e-3, 2.11e-3]   # Третє вимірювання
])

# Таблиця виміряних значень h_i' для червоного і зеленого світлофільтрів (у метрах)
h_table = np.array([
    [0.61e-3, 0.61e-3],  # Перше вимірювання
    [0.62e-3, 0.60e-3],  # Друге вимірювання
    [0.61e-3, 0.58e-3]   # Третє вимірювання
])

# ============= X =============

# Абсолютна похибка x_i для кожного світлофільтра
delta_X_vector = np.sqrt(np.var(X_table, ddof=1, axis=0) / X_table.shape[0]) * STUDENT_COEF
delta_X = np.mean(delta_X_vector)  # Середнє значення абсолютної похибки
print(f"Абсолютна похибка x_i, мм: {delta_X * 1e3:.3f}")

# Відносна похибка x_i для кожного світлофільтра
relivate1_X = delta_X_vector[0] / np.mean(X_table[:, 0]) * 100  # Для червоного світлофільтра
relivate2_X = delta_X_vector[1] / np.mean(X_table[:, 1]) * 100  # Для зеленого світлофільтра

# Середнє значення відносної похибки x_i
relivate_X = (relivate1_X + relivate2_X) / 2
print(f"Відносна похибка x_i, %: {relivate_X:.3f}")

# ============= h' =============

# Абсолютна похибка h_i' для кожного світлофільтра
delta_h_vector = np.sqrt(np.var(h_table, ddof=1, axis=0) / h_table.shape[0]) * STUDENT_COEF
delta_h = np.mean(delta_h_vector)  # Середнє значення абсолютної похибки
print(f"\nАбсолютна похибка h, мм: {delta_h * 1e3:.3f}")

# Відносна похибка h_i' для кожного світлофільтра
relivate1_h = delta_h_vector[0] / np.mean(h_table[:, 0]) * 100  # Для червоного світлофільтра
relivate2_h = delta_h_vector[1] / np.mean(h_table[:, 1]) * 100  # Для зеленого світлофільтра

# Середнє значення відносної похибки h_i'
relivate_h = (relivate1_h + relivate2_h) / 2
print(f"Відносна похибка h: {relivate_h:.3f}")

# ============= lambda =============

# Середнє значення ширини інтерференційної смуги (Delta x)
mean_Delta_x = 0.229e-3  # У метрах
delta_d = delta_F = 0.5e-3  # Абсолютна похибка вимірювань d і F (у метрах)
mean_h = 0.605e-3  # Середнє значення h' (у метрах)
delta_Delta_x = delta_X  # Абсолютна похибка Delta x

# Виміряні значення F і d (у метрах)
F = 145.0e-3
d = 665.57e-3

# Абсолютна похибка довжини хвилі lambda (за формулою для похибок)
delta_lambda = math.sqrt(
    (mean_h * (d - F)**2 * delta_Delta_x / (d**2 * F))**2 +  # Вклад похибки Delta x
    (mean_Delta_x * (d - F)**2 * delta_h / (d**2 * F))**2 +  # Вклад похибки h'
    (2 * mean_Delta_x * mean_h * (d - F) * delta_d / d**3)**2 +  # Вклад похибки d
    (mean_Delta_x * mean_h * (d**2 - F**2) * delta_F / (d**2 * F**2))**2  # Вклад похибки F
)
delta_lambda = round(delta_lambda * 1e9, 2)  # Переводимо в нанометри та округлюємо

# Відносна похибка довжини хвилі lambda (за формулою для відносних похибок)
relivate_lambda = math.sqrt(
    (delta_Delta_x / mean_Delta_x)**2 +  # Вклад відносної похибки Delta x
    (delta_h / mean_h)**2 +  # Вклад відносної похибки h'
    ((2 / d - 2 / (d - F)) * delta_d)**2 +  # Вклад відносної похибки d
    ((1 / F + 2 / (d - F)) * delta_F)**2  # Вклад відносної похибки F
) * 100
relivate_lambda = round(relivate_lambda, 2)  # Округлюємо до двох знаків після коми

# Виведення результатів для похибок lambda
print(f"\nАбсолютна похибка lambda, нм: {delta_lambda}")
print(f"Відносна похибка lambda, %: {relivate_lambda}")