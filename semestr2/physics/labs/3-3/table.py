import numpy as np
from tabulate import tabulate

# CONSTANTS
L = 450e-3  # Відстань від щілини до екрана (в метрах)
b = 0.12e-3  # Ширина щілини (в метрах)
b_min = 0.03e-3  # Мінімальна ширина щілини (в метрах)
b_max = 0.21e-3  # Максимальна ширина щілини (в метрах)
Lambda = 0.63e-6  # Довжина хвилі лазера (в метрах)
o_Lambda = 1 / Lambda  # Обернена довжина хвилі (1/метр)

# First Table

# Масив координат фотоприймача (в міліметрах)
X_vector = np.array([0, 0.4, 1, 2, 4, 5, 6, 7, 8, 8.5, 9, 10, 10.6, 11, 11.6, 13, 13.8])

# Масив показів вольтметра (в поділках)
U_vector = np.array([2600, 2200, 2000, 800, 40, 60, 120, 60, 20, 30, 45, 25, 15, 20, 30, 10, 15])

# Обчислення кутів дифракції (в радіанах)
phi_vector = X_vector * 1e-3 / L  # Переводимо X в метри та ділимо на L

# Теоретичні значення відносної інтенсивності (формула дифракції)
I_theor = np.square(np.sin(np.pi * b * o_Lambda * np.sin(phi_vector)) / 
                    (np.pi * b * o_Lambda * np.sin(phi_vector)))

# Експериментальні значення відносної інтенсивності
I_exp = U_vector / 2600  # Нормалізація на максимальне значення

# Виведення першої таблиці
print(f"\n{'Перша таблиця':^50}")
print(tabulate(
    np.array([X_vector, phi_vector, I_theor, I_exp]).T,  # Транспонування для табличного вигляду
    headers=["X, mm", "phi, rad", "I_theor", "I_exp"],  # Заголовки стовпців
    tablefmt="fancy_grid",  # Формат таблиці
    floatfmt=".4f",  # Формат чисел (4 знаки після коми)
))

# Second Table

# Новий масив координат фотоприймача (в міліметрах)
X_vector = np.array([0, 2, 4, 6.5, 9.5, 12, 15])

# Нова відстань від щілини до екрана (в метрах)
L = 270e-3

# Обчислення sin(phi) для кожного X
sin_vector = X_vector / np.sqrt(X_vector**2 + L**2)

# Обчислення кутів phi (в радіанах) через arcsin
phi_vector = np.arcsin(sin_vector)

# Виведення другої таблиці
print(f"\n{'Друга таблиця':^50}")
print(tabulate(
    np.array([X_vector, phi_vector, sin_vector]).T,  # Транспонування для табличного вигляду
    headers=["X, mm", "phi", "sin(phi)"],  # Заголовки стовпців
    tablefmt="fancy_grid",  # Формат таблиці
    floatfmt=".6f",  # Формат чисел (6 знаків після коми)
))

# Third Table Work

# Масив кутів phi (в радіанах) для третьої таблиці
phi_vector = np.array([0.0111, 0.0133, 0.0156, 0.0178, 0.0200, 0.0236, 0.0258, 0.0289])

# Масив порядкових номерів максимумів (m)
m_vector = np.array([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])

# Лінійна апроксимація залежності phi*b від m
(lambda_var, intercept), residuals, *_ = np.polyfit(m_vector, phi_vector * b, 1, full=True)

# Обчислення залишкової суми квадратів
residual_sum_of_squares = residuals[0]

# Обчислення середньоквадратичної похибки (RMSE)
rmse = np.sqrt(residual_sum_of_squares / len(phi_vector))

# Виведення результатів для довжини хвилі
print(f"\nλ: {lambda_var*1e9:.2f} нм")  # Довжина хвилі в нанометрах
print(f"delta λ = {rmse*1e9:.2f} нм")  # Похибка довжини хвилі в нанометрах

# Обчислення відношення мінімальної ширини щілини до довжини хвилі
print(f"\nВідношення b_min / λ: {round(b_min / lambda_var, 2)}")

# Обчислення відношення максимальної ширини щілини до довжини хвилі
print(f"Відношення b_max / λ: {round(b_max / lambda_var, 2)}")

# Масив значень sin(phi) для четвертої таблиці
sin_vector = np.array([0, 0.991010, 0.997730, 0.999138, 0.999596, 0.999747, 0.999838])

# Масив порядкових номерів максимумів (m)
m_vector = np.array([0, 1, 2, 3, 4, 5, 6])

# Лінійна апроксимація залежності m від sin(phi)
(coef, intercept), residuals, *_ = np.polyfit(sin_vector, m_vector, 1, full=True)

# Обчислення залишкової суми квадратів
residual_sum_of_squares = residuals[0]

# Обчислення середньоквадратичної похибки (RMSE)
rmse = np.sqrt(residual_sum_of_squares / len(sin_vector))

# Виведення результатів для періоду решітки
print(f"\nd: {lambda_var/coef*1e10:.2f} мкм")  # Період решітки в мікрометрах
print(f"delta d = {rmse:.2f} мкм")  # Похибка періоду решітки в мікрометрах
