# === ЛР4: акуратна фазорна діаграма UR + UL + UC = U ===
import numpy as np
import cmath as cm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# ---------- дані ----------
UR, UL, UC, U = 2.95, 5.60, 13.12, 10.40     # модулі (В)
fiR, fiL, fiC, fi = 0.00, 51.31, -76.09, 45  # кути (градуси, відносно I уздовж +x)

# Якщо True — будуємо загальний U як суму UR+UL+UC (гарантовано закриє полігон)
ENFORCE_CLOSURE = True

deg = np.deg2rad
rect = lambda mag, ang_deg: cm.rect(mag, deg(ang_deg))

# Фазори (ВАЖЛИВО: якщо fiC вже від’ємний, то НЕ міняємо знак при переведенні)
UR_ph = rect(UR, fiR)
UL_ph = rect(UL, fiL)
UC_ph = rect(UC, fiC)

# Сума
U_sum = UR_ph + UL_ph + UC_ph
U_ph  = U_sum if ENFORCE_CLOSURE else rect(U, fi)

# Кути для підписів
phiL = fiL
phiC = fiC
phiU = np.rad2deg(np.angle(U_ph))

# Кумулятивні точки для head-to-tail
pts = [(0.0, 0.0)]
for vec in (UR_ph, UL_ph, UC_ph):
    pts.append((pts[-1][0] + vec.real, pts[-1][1] + vec.imag))

# ---------- малювання ----------
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal', 'box')

def draw_vec(start, vec, label, color, lw=2.4, head=0.20, text_pos='head', dy=-0.30):
    end = (start[0] + vec.real, start[1] + vec.imag)
    arrow = FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=12,
                            linewidth=lw, color=color)
    ax.add_patch(arrow)
    if text_pos == 'head':
        x, y = end[0] + 0.03*vec.real, end[1] + 0.03*vec.imag
    elif text_pos == 'mid-below':
        x, y = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + dy
    ax.text(x, y, label, color=color, fontsize=12)

def draw_angle_signed(radius, start_deg, end_deg, color, label,
                      lw=2.2, fsize=13, label_scale=1.06):
    # Плавна дуга з урахуванням напряму (може бути й у від’ємний бік)
    arc_deg = np.linspace(start_deg, end_deg, 200)
    arc = deg(arc_deg)
    ax.plot(radius*np.cos(arc), radius*np.sin(arc), color=color, lw=lw)
    mid = deg((start_deg + end_deg) / 2.0)
    ax.text(label_scale*radius*np.cos(mid), label_scale*radius*np.sin(mid),
            label, color=color, fontsize=fsize)

# Вектори
draw_vec((0, 0), UR_ph, "UR", "orange", text_pos='mid-below', dy=-0.8)
draw_vec(pts[1], UL_ph, "UL", "blue")
draw_vec(pts[2], UC_ph, "UC", "green")
draw_vec((0, 0), U_ph,  "U",  "red")

# Вектор I (уздовж +x)
I_len = max(UR, UL, UC, abs(U_ph)) * 0.45
draw_vec((0, 0), complex(I_len, 0.0), "I", "magenta")

# Кути відносно осі I (+x): φL (>0), φC (<0), φ (знак за сумою)
draw_angle_signed(radius=3.2, start_deg=0, end_deg=phiL, color='blue',  label='φL')
draw_angle_signed(radius=3.0, start_deg=0, end_deg=phiC, color='green', label='φC')
draw_angle_signed(radius=3.6, start_deg=0, end_deg=phiU, color='red',   label='φ')

# Оформлення
ax.axhline(0, color='gray', lw=0.9)
ax.axvline(0, color='gray', lw=0.9)
ax.set_xlabel("Дійсна вісь")
ax.set_ylabel("Уявна вісь")
ax.set_title("UR + UL + UC = U")

rad = max(UR, UL, UC, abs(U_ph)) * 1.55
ax.set_xlim(-rad, rad)
ax.set_ylim(-rad, rad)
plt.grid(True, alpha=0.6)
plt.tight_layout()
plt.show()
