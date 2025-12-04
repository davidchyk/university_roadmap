import math
import numpy as np
import matplotlib.pyplot as plt

# == Розрахунок значень ==

S, N = 1, 6

E = 10 + S
R = E*10 + S*100 + N
L = S*0.1 + N*0.1
R_k = S*10 + N + 100

print(f"E = {E} В")
print(f"R = {R} Ом")
print(f"L = {L} Гн")
print(f"R_k = {R_k} Ом")

tau_1 = L / (R + R_k)
T = 10*tau_1
frequency = math.ceil(1 / T)

print(f"tau_1 = {tau_1:.6f} c")
print(f"T = {T:.5f} c")
print(f"frequency = {frequency} Гц")

U_L_y = 3.8939
U_R_y = 7.1058

r_k = R * U_L_y / U_R_y

print(f"r_k = {r_k:.2f} Ом")

# Побудова графіків

t_max = 5 * tau_1
t = np.linspace(0, t_max, 1000)

# === 1) Режим №1 ==========================================

u_L1 = (E * R_k) / (R + R_k) + (E * R) / (R + R_k) * np.exp(-(R - R_k) / L * t)
u_R1 = (E * R) / (R + R_k) * (1 - np.exp(-(R + R_k) / L * t))

plt.figure()
plt.plot(t, u_L1, label=r'$u_L^{(1)}(t)$')
plt.plot(t, u_R1, label=r'$u_R^{(1)}(t)$')
plt.title(r'$u_L^{(1)}(t),\, u_R^{(1)}(t)$')
plt.xlabel('t, c')
plt.ylabel(r'$u(t),\, \text{В}$')
plt.grid(True)
plt.legend()

# === 2) Режим №2 ==========================================

u_L2 = -(E * R) / (R + R_k) * np.exp(-(R + R_k) / L * t)
u_R2 =  (E * R) / (R + R_k) * np.exp(-(R + R_k) / L * t)

plt.figure()
plt.plot(t, u_L2, label=r'$u_L(t)$')
plt.plot(t, u_R2, label=r'$u_R(t)$')
plt.title(r'$u_L(t),\, u_R(t)$')
plt.xlabel('t, c')
plt.ylabel(r'$u(t),\, \text{В}$')
plt.grid(True)
plt.legend()

plt.show()