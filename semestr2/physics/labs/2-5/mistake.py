from math import sqrt, log

R = 91000 # Опір Rд, Ом
r_OUT = 0.09 # Зовнішній радіус, м
r_IN = 0.0055 # Внутрішній радіус, м
U0 = 9.0545 # U0, В

S_I = 0.000001 # Похибка I
S_R = 910 # Похибка Rд
S_r = 0.0005 # Похибка зовнішнього радіусу
S_U0 = 0.09 # Похибка U0
S_r_IN = 0.0001 # Похибка внутрішнього радіусу

# Список радіусів в метрах
r_table = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08]

# Список експериментальних напруженостей ел. поля, В/м
E_exp_table = [
    178.13250,
    234.55250,
    129.90250,
    95.32250,
    73.25500,
    61.88000,
    48.91250,
    45.04500
]

# Список виміряних I, мкА
I_table = [79.7, 78.8, 80.7, 80.5,
    53.6, 55.1, 53.8, 54.1,
    39.8, 40.1, 40.1, 39.5,
    29.4, 29.2, 29.3, 29.7,
    21.6, 21.5, 21.4, 20.9,
    14.8, 14.6, 14.4, 14.4,
    8.9, 9.3, 9.2, 9.3,
    4.3, 4.2, 4.2, 4.2]

# Знаходжу середній радіус в метрах
r = adr_r = sum(r_table)/len(r_table)

# Знаходжу середню експериментальну напруженість ел. поля
adr_e = sum(E_exp_table)/len(E_exp_table)

# Знаходжу середню силу струму I, А (тому що множу на 1e-6)
adr_I = sum(I_table)/len(I_table) * 1e-6

# Формула розрахунку похибки I
def I_mistake():

    abs_result = 0
    n = len(I_table)

    for i in range(n): abs_result = abs_result + (I_table[i]* 1e-6 - adr_I)**2
    abs_result = abs_result/(n**2-n)

    abs_result = sqrt(abs_result)
    abs_result = abs_result * 1.68
    relative = abs_result / adr_I * 100

    return abs_result, relative

# Формула розрахунку похибки U_expr
def U_expr_mistake():

    abs_result = sqrt((R*S_I)**2 + (adr_I*S_R)**2)
    relative = sqrt((S_I/adr_I)**2  + (S_R/R)**2) * 100

    return abs_result, relative

# Формула розрахунку похибки U_theor
def U_theor_mistake():

    a1 = log(r_OUT/r)*S_U0/log(r_OUT/r_IN)
    a2 = U0 * log(r/r_IN) * S_r/(r_OUT*(log(r_OUT/r_IN)**2))
    a3 = U0 * log(r_OUT/r) * S_r_IN/(r_IN*(log(r_OUT/r_IN)**2))
    a4 = U0 * S_r/(r*log(r_OUT/r_IN))

    r1 = S_U0/U0
    r2 = S_r/((1/(r*log(r_OUT/r))-1/(r*log(r_OUT/r_IN)))*r_OUT)
    r3 = S_r_IN/(r_IN*log(r_OUT/r_IN))
    r4 = S_r/(r*log(r_OUT/r))

    abs_result = sqrt(a1**2 + a2**2 + a3**2 + a4**2)
    relative = sqrt(r1**2 + r2**2 + r3**2 + r4**2) * 100

    return abs_result, relative

# Формула розрахунку похибки E_expr
def E_expr_mistake():

    abs_result = 0
    n = len(E_exp_table)

    for i in range(n): abs_result = abs_result + (adr_e - E_exp_table[i])**2
    abs_result = abs_result/(n**2-n)

    abs_result = sqrt(abs_result)
    abs_result = abs_result * 1.68
    relative = abs_result / adr_e * 100

    return abs_result, relative

# Формула розрахунку похибки E_theor
def E_theor_mistake():

    a1 = S_U0/(r*log(r_OUT/r_IN))
    a2 = S_r * U0/(r*r_OUT*(log(r_OUT/r_IN))**2)
    a3 = U0 * S_r_IN/(r*r_OUT*(log(r_OUT/r_IN))**2)
    a4 = S_r * U0/(r**2*log(r_OUT/r_IN))

    r1 = S_U0/U0
    r2 = S_r/(r_OUT*log(r_OUT/r_IN))
    r3 = S_r_IN/(r_IN*log(r_OUT/r_IN))
    r4 = S_r/r

    abs_result = sqrt(a1**2 + a2**2 + a3**2 + a4**2)
    relative = sqrt(r1**2 + r2**2 + r3**2 + r4**2) * 100

    return abs_result, relative

#Вивід результатів
print(f"Похибка I: абсолютна = {I_mistake()[0]*1000000:.3f} мкА, відн.похибка ~ {I_mistake()[1]:.2f}%")
print(f"Похибка U_expr: абсолютна = {U_expr_mistake()[0]:.2f} В, відн.похибка ~ {U_expr_mistake()[1]:.2f}%")
print(f"Похибка U_theor: абсолютна = {U_theor_mistake()[0]:.2f} В, відн.похибка ~ {U_theor_mistake()[1]:.2f}%")
print(f"Похибка E_expr: абсолютна = {E_expr_mistake()[0]:.2f} В/м, відн.похибка ~ {E_expr_mistake()[1]:.2f}%")
print(f"Похибка E_theor: абсолютна = {E_theor_mistake()[0]:.2f} В/м, відн.похибка ~ {E_theor_mistake()[1]:.2f}%")