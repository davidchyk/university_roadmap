import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def fourier_series_trig_2pi_rounded(f, t, n_terms, decimals=3):
    """
    2π-періодичний тригонометричний ряд Фур'є для f(t), заданої на [0, 2π].

    Повертає:
        S_num   – ряд з ОКРУГЛЕНИМИ коефіцієнтами (SymPy-вираз)
        S_exact – "точний" (символьний) ряд

    УВАГА:
        Всі гармонічні коефіцієнти a_n, b_n ДОДАТКОВО поділені на sqrt(2),
        тобто інтерпретуються як діючі значення.
        a0 (DC-компонента) не масштабується.
    """

    # ---- точні коефіцієнти ----
    a0 = (1/sp.pi) * sp.integrate(f, (t, 0, 2*sp.pi))
    a0 = sp.simplify(a0)

    a_list = []
    b_list = []

    # множник для переходу до діючого значення
    rms_factor = 1/sp.sqrt(2)

    for n in range(1, n_terms + 1):
        an = (1/sp.pi) * sp.integrate(f * sp.cos(n*t), (t, 0, 2*sp.pi))
        bn = (1/sp.pi) * sp.integrate(f * sp.sin(n*t), (t, 0, 2*sp.pi))

        # одразу зберігаємо ДІЮЧІ значення гармонік
        an = sp.simplify(an * rms_factor)
        bn = sp.simplify(bn * rms_factor)

        a_list.append(an)
        b_list.append(bn)

    # ---- будуємо точний ряд (з уже поділеними на sqrt(2) коеф.) ----
    S_exact = a0/2
    for n in range(1, n_terms + 1):
        S_exact += a_list[n-1]*sp.cos(n*t) + b_list[n-1]*sp.sin(n*t)

    # ---- будуємо числовий ряд з округленням ----
    def r(x):
        return round(float(x.evalf()), decimals)

    a0r = r(a0)
    S_num = a0r/2

    for n in range(1, n_terms + 1):
        anr = r(a_list[n-1])
        bnr = r(b_list[n-1])

        if anr != 0:
            S_num += anr * sp.cos(n*t)
        if bnr != 0:
            S_num += bnr * sp.sin(n*t)

    # ---- красивий вивід ----
    terms_str = [f"{a0r/2:.{decimals}f}"]
    for n in range(1, n_terms + 1):
        anr = r(a_list[n-1])
        bnr = r(b_list[n-1])

        if anr != 0:
            terms_str.append(f"{anr:+.{decimals}f}*cos({n}*t)")
        if bnr != 0:
            terms_str.append(f"{bnr:+.{decimals}f}*sin({n}*t)")

    pretty = "S(t) ≈ " + " ".join(terms_str)
    print(pretty)

    return S_num, S_exact

t = sp.symbols('t')

f = sp.Piecewise(
    (t/sp.pi, (t >= 0) & (t <= sp.pi)),          # 0 ≤ t ≤ π
    (-t/sp.pi + 2, (t > sp.pi) & (t <= 2*sp.pi)) # π < t ≤ 2π
)

n_terms = 5
S_num_expr, S_exact = fourier_series_trig_2pi_rounded(f, t, n_terms=n_terms, decimals=3)

# --- Малюємо графік f(t) і S(t) на [0, 2π] ---

# Перетворюємо SymPy-вирази в числові функції (для numpy)
f_num = sp.lambdify(t, f, 'numpy')
S_num = sp.lambdify(t, S_num_expr, 'numpy')

# Точки по осі t
x_vals = np.linspace(0, 2*np.pi, 1000)

# Значення функцій
y_f = f_num(x_vals)
y_S = S_num(x_vals)

plt.figure(figsize=(9, 5))
plt.plot(x_vals, y_f, label='f(t) (оригінал)', linewidth=2)
plt.plot(x_vals, y_S, label=f'Ряд Фур’є, N={n_terms}', linestyle='--')

plt.xlabel('t')
plt.ylabel('значення')
plt.title('Кусочна функція f(t) і її часткова сума ряду Фур’є')
plt.xlim(0, 2*np.pi)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()