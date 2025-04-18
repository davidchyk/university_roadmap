import numpy as np
from tabulate import tabulate
import math

r1_table = np.array(list(range(0, 11)))
r2_table = np.array(list(range(11, 21)))

E1_table = 5395.08 * (1 - np.cos(10.47 * r1_table / 100))
E2 = 2697.54

F1_table = -5395.08 * (r1_table / 100 - 0.095 * np.sin(10.47 * r1_table / 100))
F2_table = -2967.54 * (-0.065 + r2_table / 100)

# Формування таблиці
data = []
for r in range(0, 21):
    if r <= 10:
        E = E1_table[r]
        F = F1_table[r]
    else:
        E = E2
        F = F2_table[r - 11]
    data.append([r, E, F])

# Вивід таблиці
headers = ["r, см", "E, В/м", "F, В"]
print(tabulate(data, headers=headers, tablefmt="fancy_grid", stralign="center", floatfmt=".2f"))

for r in r1_table:

    R = r / 100

    print(f"E({R}) = E1({R}) = 5395,08 • (1 - cos(10,47 • {R})) = 5395,08 • (1 - {math.cos(10.47 * R):.6f}) = 5395,08 • {1 - math.cos(10.47 * R):.6f} = {E1_table[r]:.2f} В/м".replace('.', ','))
    print(f"F({R}) = F1({R}) = -5395,08 • ({R} - 0,095 • sin(10,47 • {R})) = -5395,08 • ({R} - {0.095 * math.sin(10.47 * R):.6f}) = -5395,08 • {R - 0.095 *  math.sin(10.47 * R):.6f} = {F1_table[r]:.2f} В".replace('.', ','))
    print("\n")

print("\n\n")

for r in r2_table:

    R = r / 100

    print(f"F({R}) = F2({R}) = -2697,54 • (-0,065 + {R}) = -2697,54 • ({-0.065 + R:.3f}) = {F2_table[r - 11]:.2f} В".replace('.', ','))
    print("\n")