import math
import numpy as np
import matplotlib.pyplot as plt

# == Розрахунок значень ==

S, N = 1, 7

E = 10 + S
R = 10*S + N
C = (100*S - N*2) * 1e-6

print(f"E = {E} В")
print(f"R = {R} Ом")
print(f"C = {C} мкФ")

tau = R*C
T = 10*tau
frequency = math.ceil(1 / T)

print(f"tau = {tau} с")
print(f"T = {T:.5f} с")
print(f"frequency = {frequency} Гц")

# == Побудова графіків аналітичних функцій ==

graph_tau = 1.4796e-3

# Час: від 0 до 5τ (можеш змінити за бажанням)
t_max = 5 * graph_tau
t = np.linspace(0, t_max, 1000)

# Функції
u = E * (1 - np.exp(-t / graph_tau))   # u_C(t)
i = (E / R) * np.exp(-t / graph_tau)   # i(t)

# --- Графік напруги u_C(t) ---
plt.figure()
plt.plot(t, u)
plt.title(r'$u_C(t) = E\left(1 - e^{-t/RC}\right)$')
plt.xlabel('t, с')
plt.ylabel('u_C(t), В')
plt.grid(True)

# --- Графік струму i(t) ---
plt.figure()
plt.plot(t, i)
plt.title(r'$i(t) = \frac{E}{R} e^{-t/RC}$')
plt.xlabel('t, с')
plt.ylabel('i(t), A')
plt.grid(True)

# Функції розряду
u2 = E * np.exp(-t / graph_tau)        # u_C(t) = E e^{-t/RC}
i2 = -(E / R) * np.exp(-t / graph_tau) # i(t) = -(E/R) e^{-t/RC}

# --- Графік напруги u_C(t) ---
plt.figure()
plt.plot(t, u2)
plt.title(r'$u_C(t) = E e^{-t/RC}$')
plt.xlabel('t, c')
plt.ylabel(r'$u_C(t),\,\text{В}$')
plt.grid(True)

# --- Графік струму i(t) ---
plt.figure()
plt.plot(t, i2)
plt.title(r'$i(t) = -\frac{E}{R} e^{-t/RC}$')
plt.xlabel('t, c')
plt.ylabel(r'$i(t),\,\text{A}$')
plt.grid(True)

plt.show()