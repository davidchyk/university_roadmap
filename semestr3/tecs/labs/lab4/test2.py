# === ЛР4: UR + UL + UC = U — охайні дуги φ ===
import numpy as np
import cmath as cm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Wedge

# ---------- дані ----------
UR, UL, UC, U = 2.95, 5.6, 13.12, 10.4
fiR, fiL, fiC = 0.0, 51.31, -76.09

deg = np.deg2rad
rect = lambda mag, ang_deg: cm.rect(mag, deg(ang_deg))

# фазирування (ВАЖЛИВО: fiC уже від’ємний — без зміни знаку!)
UR_ph = rect(UR, fiR)
UL_ph = rect(UL, fiL)
UC_ph = rect(UC, fiC)

# сумарний вектор і його фаза (для дуги φ)
U_ph  = UR_ph + UL_ph + UC_ph
phiU  = np.rad2deg(np.angle(U_ph))

# точки для head-to-tail
pts = [(0.0, 0.0)]
for v in (UR_ph, UL_ph, UC_ph):
    pts.append((pts[-1][0] + v.real, pts[-1][1] + v.imag))

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal', 'box')

def draw_vec(start, vec, label, color, lw=2.4, text_pos='head', dy=-0.30):
    end = (start[0] + vec.real, start[1] + vec.imag)
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=12,
                                 linewidth=lw, color=color))
    if text_pos == 'head':
        x, y = end[0] + 0.03*vec.real, end[1] + 0.03*vec.imag
    elif text_pos == 'mid-below':
        x, y = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + dy
    ax.text(x, y, label, color=color, fontsize=12)

# --- НОВЕ: акуратні дуги (і для від’ємних кутів теж) ---
def draw_angle_arc(radius, angle_deg, color, label, lw=2.2, fsize=13, label_scale=1.06):
    """
    Малює ідеальну колову дугу від 0° до angle_deg (з урахуванням знаку).
    Без стрілок — напрямок не позначається (тільки геометрія), зате завжди гладко.
    """
    theta1 = min(0.0, angle_deg)
    theta2 = max(0.0, angle_deg)
    arc = Wedge(center=(0, 0), r=radius, theta1=theta1, theta2=theta2,
                width=0.0, fill=False, edgecolor=color, linewidth=lw)
    ax.add_patch(arc)
    # підпис у середині дуги
    mid = np.deg2rad((theta1 + theta2) / 2.0)
    ax.text(label_scale*radius*np.cos(mid), label_scale*radius*np.sin(mid),
            label, color=color, fontsize=fsize)

# вектори
draw_vec((0, 0), UR_ph, "UR", "orange", text_pos='mid-below', dy=-0.8)
draw_vec(pts[1], UL_ph, "UL", "blue")
draw_vec(pts[2], UC_ph, "UC", "green")
draw_vec((0, 0), U_ph,  "U",  "red")

# вектор I
I_len = max(UR, UL, UC, abs(U_ph)) * 0.45
draw_vec((0, 0), complex(I_len, 0.0), "I", "magenta")

# --- дуги (усі однаково гладкі/красиві) ---
#
# оформлення
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
