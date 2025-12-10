# Offline part

R4 = 50
L4 = 60e-3
C4 = 3e-6
R0 = 50
R_k = 35.5

R_kr = 2*(L4 / C4) ** 0.5

print(f"R_kr = {R_kr:.2f} Ом")

R_kr_all = R_k + R4

omega = 1 / (L4 * C4) ** 0.5
delta = R_kr_all / (2 * L4)

print(f"omega = {omega:.2f} рад/с")
print(f"delta = {delta:.2f} рад/с")

C2 = C4 / (4 - 3*R_kr_all**2 / omega**2)

print(f"C2 = {C2*1e6:.2f} мкФ")

## Analytical part

import numpy as np
import matplotlib.pyplot as plt

E = 8
omega0 = omega
omega_v = (omega0**2 - delta**2) ** 0.5

T0 = 2*np.pi / omega_v
t_max = 5 * T0

### ----- КОЕФІЦІЄНТИ ПЕРЕД e^{-δt} * sin(ω_v t) -----
A_i = E / (omega_v * L4)
A_L = E * (omega0 / omega_v)
A_C = E * (omega0 / omega_v)
A_R = E * R4 / (omega_v * L4)

### ----- ДРУК ФУНКЦІЙ У ВИГЛЯДІ "coef * e^(-delta t) * sin(omega_v t ...)" -----
print(f"i(t)  = {A_i:.5g} * e^(-{delta:.5g} t) * sin({omega_v:.5g} t)")
print(f"u_L(t) = {A_L:.5g} * e^(-{delta:.5g} t) * sin({omega_v:.5g} t + π/2)")
print(f"u_C(t) = {E:.5g} + {A_C:.5g} * e^(-{delta:.5g} t) * sin({omega_v:.5g} t - π/2)")
print(f"u_R(t) = {A_R:.5g} * e^(-{delta:.5g} t) * sin({omega_v:.5g} t)")

### --- час ---
t = np.linspace(0, t_max, 5000)

### --- функції ---
def i_t(t):
    return (E / (omega_v * L4)) * np.exp(-delta * t) * np.sin(omega_v * t)

def u_L_t(t):
    return E * (omega0 / omega_v) * np.exp(-delta * t) * np.sin(omega_v * t + np.pi/2)

def u_C_t(t):
    return E + E * (omega0 / omega_v) * np.exp(-delta * t) * np.sin(omega_v * t - np.pi/2)

def u_R_t(t):
    return i_t(t) * R4

### значення
i_vals  = i_t(t)
uL_vals = u_L_t(t)
uC_vals = u_C_t(t)
uR_vals = u_R_t(t)

### --- графік ---
plt.figure()
plt.plot(t, i_vals,  label="i(t)")
plt.plot(t, uL_vals, label="u_L(t)")
plt.plot(t, uC_vals, label="u_C(t)")
plt.plot(t, uR_vals, label="u_R(t)")
plt.xlabel("t, s")
plt.ylabel("Amplitude")
plt.title("RLC transient")
plt.grid(True)
plt.legend()
plt.show()

delta  = (R4 + R_k + R0) / (2 * L4)

# ---------- КОЕФІЦІЄНТИ У ФУНКЦІЯХ ----------
A_i = -E / (omega_v * L4)
A_L =  E * (omega0 / omega_v)
A_C =  E * (omega0 / omega_v)
A_R = -E * R4 / (omega_v * L4)

print("\n---")

# ---------- ДРУК ЯВНИХ ФОРМУЛ ----------
print(f"i(t)  = {A_i:.5g} * exp(-{delta:.5g} * t) * sin({omega_v:.5g} * t)")
print(f"u_L(t) = {A_L:.5g} * exp(-{delta:.5g} * t) * "
      f"sin({omega_v:.5g} * t - pi/2)")
print(f"u_C(t) = {A_C:.5g} * exp(-{delta:.5g} * t) * "
      f"sin({omega_v:.5g} * t + pi/2)")
print(f"u_R(t) = {A_R:.5g} * exp(-{delta:.5g} * t) * sin({omega_v:.5g} * t)")

def i_t(t):
    return A_i * np.exp(-delta * t) * np.sin(omega_v * t)

def u_L_t(t):
    return A_L * np.exp(-delta * t) * np.sin(omega_v * t - np.pi/2)

def u_C_t(t):
    return A_C * np.exp(-delta * t) * np.sin(omega_v * t + np.pi/2)

def u_R_t(t):
    return A_R * np.exp(-delta * t) * np.sin(omega_v * t)

Tv = 2 * np.pi / omega_v
t_max = 5 * Tv
t = np.linspace(0, t_max, 5000)

# ---------- ОБЧИСЛЕННЯ ЗНАЧЕНЬ ----------
i_vals  = i_t(t)
uL_vals = u_L_t(t)
uC_vals = u_C_t(t)
uR_vals = u_R_t(t)

# ---------- ГРАФІК ----------
plt.figure()
plt.plot(t, i_vals,  label="i(t)")
plt.plot(t, uL_vals, label="u_L(t)")
plt.plot(t, uC_vals, label="u_C(t)")
plt.plot(t, uR_vals, label="u_R(t)")
plt.xlabel("t, s")
plt.ylabel("Amplitude")
plt.title("RLC transient")
plt.grid(True)
plt.legend()
plt.show()