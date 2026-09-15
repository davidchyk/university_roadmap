import math
import numpy as np

def pol2rect(mag, deg):
    """Перехід з полярної форми (магнітуда, градуси) в комплексне число."""
    rad = math.radians(deg)
    return complex(mag*math.cos(rad), mag*math.sin(rad))

def cabs_deg(z):
    """(модуль, фаза в градусах) для комплексного числа."""
    return abs(z), math.degrees(math.atan2(z.imag, z.real))

# Вхідні дані

E = 17+0j # В

R = 220 # Ом
f = 50 # Гц

Z_L = 142 # Ом
phi_L = 42 # град

Z_C = 240 # Ом
phi_C = -83 # град

# Додатковий розрахунок активних та реактивних складових імпедансів

omega = 2 * math.pi * f

R_L = Z_L * round(math.cos(math.radians(phi_L)), 3)
X_L = Z_L * round(math.sin(math.radians(phi_L)), 3)

R_C = Z_C * round(math.cos(math.radians(phi_C)), 3)
X_C = Z_C * round(math.sin(math.radians(phi_C)), 3)

L = round(X_L / omega, 3)
C = round(-1 / (omega * X_C)*1e6, 3)

print(f"Індуктивний опір (R_L): {R_L} Ом")
print(f"Індуктивна реактивність (X_L): {X_L} Ом\n")
print(f"Ємнісний опір (R_C): {R_C} Ом")
print(f"Ємнісна реактивність (X_C): {X_C} Ом")

print(f"\nІндуктивність (L): {L} Гн")
print(f"Ємність (C): {C} мкФ\n")

Z1 = R + 0j
Z2 = R_L + 1j * X_L
Z3 = R_C + 1j * X_C

A = np.array([
    [Z1,  Z2,  0+0j],
    [Z1,  0+0j, Z3 ],
    [1+0j, -1+0j, -1+0j]
], dtype=complex)

b = np.array([E, E, 0+0j], dtype=complex)

# Розв'язок
I1, I2, I3 = np.linalg.solve(A, b)

module_I1 = round(abs(I1), 3)
module_I2 = round(abs(I2), 3)
module_I3 = round(abs(I3), 3)

phase_I1 = round(math.degrees(math.atan2(I1.imag, I1.real)), 3)
phase_I2 = round(math.degrees(math.atan2(I2.imag, I2.real)), 3)
phase_I3 = round(math.degrees(math.atan2(I3.imag, I3.real)), 3)

print(f"Результати розв'язку системи лінійних рівнянь:\n")
print(f"I1 = {round(I1.real,3)} + {round(I1.imag,3)}j = {module_I1} e^j({phase_I1}°)")
print(f"I2 = {round(I2.real,3)} + {round(I2.imag,3)}j = {module_I2} e^j({phase_I2}°)")
print(f"I3 = {round(I3.real,3)} + {round(I3.imag,3)}j = {module_I3} e^j({phase_I3}°)")

# Баланс потужностей

S_E = E * I1
S_D = I1**2 * Z1 + I2**2 * Z2 + I3**2 * Z3

print(f"\nБаланс потужностей:\n")
print(f"S_джерело = {round(S_E.real,3)} + {round(S_E.imag,3)}j = {round(abs(S_E),3)} e^j({round(math.degrees(math.atan2(S_E.imag, S_E.real)),3)}°)")
print(f"S_споживачі = {round(S_D.real,3)} + {round(S_D.imag,3)}j = {round(abs(S_D),3)} e^j({round(math.degrees(math.atan2(S_D.imag, S_D.real)),3)}°)")
print(f"Повна комплексна потужність джерела: {round(abs(S_E), 3)} Вт")

# Розрахунок комплексних напруг

U_R  = I1 * R
U_RL = I2 * R_L
U_L  = I2 * (1j * X_L)
U_RC = I3 * R_C
U_C  = I3 * (-1j * X_C)

module_U_R = round(abs(I1 * R), 3)
module_U_RL = round(abs(I2 * R_L), 3)
module_U_L = round(abs(I2 * (1j * X_L)), 3)
module_U_RC = round(abs(I3 * R_C), 3)
module_U_C = round(abs(I3 * (-1j * X_C)), 3)

print("\nРезультат обчислення комплексних напруг:")
print(f"U_R = {round(U_R.real,3)} + {round(U_R.imag,3)}j = {round(abs(U_R), 3)} e^j({round(math.degrees(math.atan2(U_R.imag, U_R.real)),3)}°)")
print(f"U_RL = {round(U_RL.real,3)} + {round(U_RL.imag,3)}j = {round(abs(U_RL), 3)} e^j({round(math.degrees(math.atan2(U_RL.imag, U_RL.real)),3)}°)")
print(f"U_L = {round(U_L.real,3)} + {round(U_L.imag,3)}j = {round(abs(U_L), 3)} e^j({round(math.degrees(math.atan2(U_L.imag, U_L.real)),3)}°)")
print(f"U_RC = {round(U_RC.real,3)} + {round(U_RC.imag,3)}j = {round(abs(U_RC), 3)} e^j({round(math.degrees(math.atan2(U_RC.imag, U_RC.real)),3)}°)")
print(f"U_C = {round(U_C.real,3)} + {round(U_C.imag,3)}j = {round(abs(U_C), 3)} e^j({round(math.degrees(math.atan2(U_C.imag, U_C.real)),3)}°)")
