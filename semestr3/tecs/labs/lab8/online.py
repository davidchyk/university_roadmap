import cmath
import numpy as np
import matplotlib.pyplot as plt

S, N = 1, 6

def solve_char_eq(delta, omega0):
    """
    Розв'язує p^2 + 2*delta*p + omega0^2 = 0
    Повертає пару (p1, p2).
    """
    a = 1
    b = 2 * delta
    c = omega0**2

    D = b**2 - 4*a*c
    sqrtD = cmath.sqrt(D)

    p1 = (-b + sqrtD) / (2*a)
    p2 = (-b - sqrtD) / (2*a)
    return p1, p2

E = 10 + S
R = E*10 + N
L = S*0.1 + N*0.01
C = (10 - N*0.1)*1e-6
R0 = 50

print(f"E = {E} В")
print(f"R = {R} Ом")
print(f"L = {L} Гн")
print(f"C = {C*1e6} мкФ")

delta = R / (2 * L)
omega_0 = 1 / (L * C) ** 0.5

tau = 1/ delta

print(f"delta = {delta:.2f} рад/с")
print(f"omega_0 = {omega_0:.2f} рад/с")

p1, p2 = solve_char_eq(delta, omega_0)

print(f"p1 = {p1:.2f} рад/с")
print(f"p2 = {p2:.2f} рад/с")
print(f"tau = {tau*1e3:.2f} мс")

R_kr = 2 * (L / C) ** 0.5
print(f"R_kr = {R_kr:.2f} Ом")

print("\nАперіодичний режим:")

R_other = 256

delta_other = (R_other + R0) / (2 * L)

print(f"delta = {delta_other:.2f} рад/с")

p1_other, p2_other = solve_char_eq(delta_other, omega_0)

tau_other = abs(1 / p1_other)

print(f"p1 = {p1:.2f} рад/с")
print(f"p2 = {p2:.2f} рад/с")
print(f"tau = {tau_other*1e3:.2f} мс")

omega_v = (omega_0**2 - delta**2) ** 0.5

print(f"\nomega_v = {omega_v:.2f} рад/с")

# ---------- Графіки

T0 = 2*np.pi / omega_v
t_max = 5 * T0

t = np.linspace(0, t_max, 5000)

### --- функції ---

def u_C_t_per(t):
    return E + E * (omega_0 / omega_v) * np.exp(-delta * t) * np.sin(omega_v * t - np.pi/2)

def u_C_t_a(t):
    return E - (E / (p2_other - p1_other)) * (p2_other * np.exp(p1_other * t) - p1_other * np.exp(p2_other * t))

uC_vals = u_C_t_per(t)
uC_vals_ap = u_C_t_a(t)

### --- графік ---
plt.figure()
plt.plot(t, uC_vals, label="u_C(t) - періодичний режим")
plt.plot(t, uC_vals_ap, label="u_C(t) - аперіодичний режим")
plt.xlabel("t, s")
plt.ylabel("Amplitude")
plt.title("RLC transient - Напруга на конденсаторі під час замикання ключа")
plt.grid(True)
plt.legend()
plt.show()