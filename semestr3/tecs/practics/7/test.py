import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def fourier_series_trig_2pi_rounded(f, t, n_terms, decimals=3, is_sqrted=False):
    """
    2π-періодичний тригонометричний ряд Фур'є для f(t), заданої на [0, 2π].

    Повертає:
        S_num   – ряд з ОКРУГЛЕНИМИ коефіцієнтами (SymPy-вираз)
        S_exact – "точний" (символьний) ряд

    УВАГА:
        Всі гармонічні коефіцієнти a_n, b_n ДОДАТКОВО поділені на sqrt(2),
        тобто інтерпретуються як діючі значення.
        a0 (DC-компонента) не масштабується.

    Форма ряду:
        S(t) = a0/2 + Σ c_n * sin(n*t + φ_n)
    """

    # ---- точні коефіцієнти ----
    a0 = (1/sp.pi) * sp.integrate(f, (t, 0, 2*sp.pi))
    a0 = sp.simplify(a0)

    a_list = []
    b_list = []

    # множник для переходу до діючого значення

    rms_factor = 1 / (sp.sqrt(2) if is_sqrted else 1)

    for n in range(1, n_terms + 1):
        an = (1/sp.pi) * sp.integrate(f * sp.cos(n*t), (t, 0, 2*sp.pi))
        bn = (1/sp.pi) * sp.integrate(f * sp.sin(n*t), (t, 0, 2*sp.pi))

        # одразу зберігаємо ДІЮЧІ значення гармонік
        an = sp.simplify(an * rms_factor)
        bn = sp.simplify(bn * rms_factor)

        a_list.append(an)
        b_list.append(bn)

    # ---- переходимо до форми c_n * sin(n*t + φ_n) ----
    c_list = []
    phi_list = []

    for an, bn in zip(a_list, b_list):
        c_n = sp.sqrt(an**2 + bn**2)
        # φ_n: tan φ = a_n / b_n => atan2(a_n, b_n)
        phi_n = sp.atan2(an, bn)

        c_list.append(sp.simplify(c_n))
        phi_list.append(sp.simplify(phi_n))

    # ---- точний ряд в sin-формі ----
    S_exact = a0/2
    for n in range(1, n_terms + 1):
        S_exact += c_list[n-1] * sp.sin(n*t + phi_list[n-1])

    # ---- будуємо числовий ряд з округленням ----
    def r(x):
        return round(float(x.evalf()), decimals)

    a0r = r(a0)
    S_num = a0r/2

    # красивий вивід
    terms_str = [f"{a0r/2:.{decimals}f}"]

    for n in range(1, n_terms + 1):
        cnr = r(c_list[n-1])
        phir = r(phi_list[n-1])

        if cnr != 0:
            S_num += cnr * sp.sin(n*t + phir)
            # синус з фазою
            terms_str.append(
                f"{cnr:+.{decimals}f}*sin({n}*t{phir:+.{decimals}f})"
            )

    pretty = "S(t) ≈ " + " ".join(terms_str)

    if is_sqrted: print(f"Розклад Фур'є для діючих значень: {pretty}\n")
    else: print(f"Розклад Фур'є для амплітудних значень: {pretty}")

    return S_num, S_exact


# ----- Далі твій код без змін -----

t = sp.symbols('t')

f = sp.Piecewise(
    (t**2/sp.pi, (t >= 0) & (t <= sp.pi)),          # 0 ≤ t ≤ π
    (-t/sp.pi + 2, (t > sp.pi) & (t <= 2*sp.pi)) # π < t ≤ 2π
)

n_terms = 100
S_num_expr_real, _ = fourier_series_trig_2pi_rounded(f, t, n_terms=n_terms, decimals=3, is_sqrted=True)
S_num_expr, _ = fourier_series_trig_2pi_rounded(f, t, n_terms=n_terms, decimals=3, is_sqrted=False)

# --- Малюємо графік f(t) і S(t) на [0, 2π] ---

# Перетворюємо SymPy-вирази в числові функції (для numpy)
f_num = sp.lambdify(t, f, 'numpy')
S_num_real = sp.lambdify(t, S_num_expr_real, 'numpy')
S_num = sp.lambdify(t, S_num_expr, 'numpy')

# Точки по осі t
x_vals = np.linspace(0, 2*np.pi, 1000)

# Значення функцій
y_f = f_num(x_vals)
y_S = S_num_real(x_vals)
g_S = S_num(x_vals)

plt.figure(figsize=(9, 5))
plt.plot(x_vals, y_f, label='f(t) (оригінал)', linewidth=2)
plt.plot(x_vals, y_S, label=f'Ряд Фур’є при N={n_terms} гармонік, діючі значення', linestyle='--')
plt.plot(x_vals, g_S, label=f'Ряд Фур’є при N={n_terms} гармонік, амлпітудні значення', linestyle='--')

plt.xlabel('t')
plt.ylabel('значення')
plt.title('Кусочна функція f(t) і її часткова сума ряду Фур’є')
plt.xlim(0, 2*np.pi)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()