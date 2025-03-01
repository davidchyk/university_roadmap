import math

##########################
# 1. Вихідні дані
##########################

# (а) Повторні вимірювання сили струму (µA)
#    Наприклад, 8 вимірювань
I_measurements = [79.7, 78.8, 80.7, 80.5,
    53.6, 55.1, 53.8, 54.1,
    39.8, 40.1, 40.1, 39.5,
    29.4, 29.2, 29.3, 29.7,
    21.6, 21.5, 21.4, 20.9,
    14.8, 14.6, 14.4, 14.4,
    8.9, 9.3, 9.2, 9.3,
    4.3, 4.2, 4.2, 4.2]

# (б) Опір R_d, його номінал і похибка (в Омах)
R_d = 91000.0
delta_R_d = 910.0    # Наприклад, ±1% від 91 кОм

# (в) Вольтметр на U0 (виміряна напруга), з похибкою ±0.09 В (1%)
U0 = 9.0545
delta_U0 = 0.09

# (г) Радіуси (в метрах) і їхні похибки
r_out = 0.09
delta_r_out = 0.0005   # Наприклад, ±0.5 мм

r_in = 0.0055
delta_r_in = 0.0001    # Наприклад, ±0.1 мм

# Точка, у якій обчислюємо U_theor(r) і E_theor(r)
r = 0.03        # 3 см
delta_r = 0.0005

##########################
# 2. Статистична обробка I
##########################

def mean_std(data):
    """ Повертає (середнє, стандартне відхилення вибірки) """
    n = len(data)
    m = sum(data)/n
    s_sq = sum((x - m)**2 for x in data)/(n - 1)
    s = math.sqrt(s_sq)
    return (m, s)

mean_I, std_I = mean_std(I_measurements)
print(f"Середнє I = {mean_I:.3f} мкА, σ_I = {std_I:.3f} мкА")

# Припустимо, що абсолютна похибка I = σ_I (не похибка середнього, а просто "розкид")
# Якщо потрібна похибка середнього, множте на t_крит. / sqrt(n)

#########################################
# 3. U_exp = I * R_d (метод диференціалів)
#########################################

# I у мікроамперах => Переведемо в ампери
I_amp = mean_I * 1e-6
delta_I_amp = std_I * 1e-6

def U_exp_and_error(Ia, dIa, Rd, dRd):
    """Повертає (U_exp, Delta U_exp) за формулою U=I*R. """
    Ue = Ia * Rd
    # Метод диференціалів
    dUe = math.sqrt( (Rd*dIa)**2 + (Ia*dRd)**2 )
    return (Ue, dUe)

U_exp_value, delta_U_exp = U_exp_and_error(I_amp, delta_I_amp, R_d, delta_R_d)

rel_U_exp = (delta_U_exp/U_exp_value)*100

print(f"U_exp = {U_exp_value:.5f} В ± {delta_U_exp:.5f} В  (відн.похибка ~ {rel_U_exp:.2f}%)")

#################################################
# 4. U_theor(r) = (U0 / ln(r_out/r_in)) * ln(r_out / r)
#    та її похибка за методом диференціалів
#################################################

def U_theor(r_val):
    return (U0 / math.log(r_out/r_in))*math.log(r_out/r_val)

def partials_U_theor(r_val):
    """
    Повертає чотири частинні похідні dU/dU0, dU/dr_out, dU/dr_in, dU/dr
    для U_theor(r).
    """
    # Для зручності
    denom = math.log(r_out/r_in)  # знаменник
    return {
      "dU0": math.log(r_out/r_val)/denom,
      "dr_out": (U0/denom)* (1/r_out)* math.log(r_val/r_in)/(denom),  # треба акуратно вивести
      "dr_in":  (U0/denom)* (1/r_in)* math.log(r_out/r_val)/(denom) , # та ж ідея
      "dr":  (U0/denom)* (-1/r_val)
    }

def U_theor_error(r_val, dU0, dr_out_, dr_in_, dr_):
    # Саме тут обчислюємо повну похибку
    d = partials_U_theor(r_val)
    # dU/dU0 * dU0:
    c1 = (d["dU0"]*dU0)**2
    # dU/dr_out * dr_out:
    c2 = (d["dr_out"]*dr_out_)**2
    # dU/dr_in * dr_in:
    c3 = (d["dr_in"]*dr_in_)**2
    # dU/dr * dr:
    c4 = (d["dr"]*dr_)**2
    return math.sqrt(c1+c2+c3+c4)

U_th = U_theor(r)
delta_U_th = U_theor_error(r, delta_U0, delta_r_out, delta_r_in, delta_r)

rel_U_th = (delta_U_th/U_th)*100

print(f"U_theor(r={r*100}см) = {U_th:.5f} В ± {delta_U_th:.5f} В  (~{rel_U_th:.2f}%)")

#################################################
# 5. E_exp(r): приклад обчислення статистики
#################################################

# Припустимо, що у нас є кілька експериментальних значень E_exp
# (наприклад, виміряних у різних точках) -> E_exp_table
E_exp_table = [178.13, 234.55, 129.90, 95.32, 73.26, 61.88, 48.91, 45.05]

mean_E, std_E = mean_std(E_exp_table)
print(f"E_exp середнє = {mean_E:.2f}, σ = {std_E:.2f} (умовні одиниці В/м)")

#################################################
# 6. E_theor(r) = [U0 / ln(r_out/r_in)] * 1/r
#    та її похибка
#################################################

def E_theor(r_val):
    return (U0 / math.log(r_out/r_in))*(1/r_val)

def partials_E_theor(r_val):
    """
    dE/dU0, dE/dr_out, dE/dr_in, dE/dr
    E(r) = (U0/ln(r_out/r_in)) * (1/r)
    """
    denom = math.log(r_out/r_in)
    return {
      "dU0": 1/(r_val*denom),
      "dr_out": - U0/(r_val * (r_out)*(denom**2)),  # треба точно вивести похідну
      "dr_in":  + U0/(r_val * (r_in)*(denom**2)),   # аналогічно
      "dr":   - (U0/(denom))*(1/(r_val**2))
    }

def E_theor_error(r_val, dU0, dr_out_, dr_in_, dr_):
    d = partials_E_theor(r_val)
    c1 = (d["dU0"]*dU0)**2
    c2 = (d["dr_out"]*dr_out_)**2
    c3 = (d["dr_in"]*dr_in_)**2
    c4 = (d["dr"]*dr_)**2
    return math.sqrt(c1+c2+c3+c4)

E_th = E_theor(r)
delta_E_th = E_theor_error(r, delta_U0, delta_r_out, delta_r_in, delta_r)
rel_E_th = (delta_E_th/E_th)*100

print(f"E_theor(r={r*100}см) = {E_th:.2f} ± {delta_E_th:.2f} (В/м) (~{rel_E_th:.2f}%)")
