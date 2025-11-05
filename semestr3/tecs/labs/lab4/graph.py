# === ЛР4: остаточна діаграма UR + UL + UC = U (UR нижче вектора, кути φ великі) ===
import numpy as np
import cmath as cm
import matplotlib.pyplot as plt

# ---------- дані ----------
UR, UL, UC, U = 2.95, 5.6, 3.12, 10.4
fiR, fiL, fiC, fi = 0, 51.31, -76.09, 45

deg = np.deg2rad
phiR, phiL, phiC, phiU = deg(fiR), deg(fiL), -deg(fiC), deg(fi)

UR_ph = cm.rect(UR, phiR)
UL_ph = cm.rect(UL, phiL)
UC_ph = cm.rect(UC, phiC)
U_ph  = cm.rect(U,  phiU)

pts = [(0.0,0.0)]
pts.append((UR_ph.real, UR_ph.imag))
pts.append((pts[-1][0]+UL_ph.real, pts[-1][1]+UL_ph.imag))
pts.append((pts[-1][0]+UC_ph.real, pts[-1][1]+UC_ph.imag))
sum_vec = UR_ph + UL_ph + UC_ph

fig, ax = plt.subplots(figsize=(8,8))
ax.set_aspect('equal','box')

def draw_vec(start, vec, label, color, lw=2.2, head=0.18, text_pos='head', dy=-0.25):
    ax.arrow(start[0], start[1], vec.real, vec.imag,
             head_width=head, length_includes_head=True, linewidth=lw, color=color)
    if text_pos == 'head':
        x = start[0] + vec.real*1.03
        y = start[1] + vec.imag*1.03
    elif text_pos == 'mid-below':
        x = start[0] + vec.real*0.5
        y = start[1] + vec.imag*0.5 + dy
    ax.text(x, y, label, color=color, fontsize=12)

# UR — підпис ще нижче, щоб не торкався вектора
draw_vec((0,0), UR_ph, "UR", "orange", text_pos='mid-below', dy=-0.8)
draw_vec(pts[1], UL_ph, "UL", "blue")
draw_vec(pts[2], UC_ph, "UC", "green")
draw_vec((0,0), U_ph,  "U",  "red")

# Вектор I
I_len = max(UR, UL, UC, U)*0.45
ax.arrow(0,0, I_len,0, head_width=0.18, length_includes_head=True, linewidth=2.2, color='magenta')
ax.text(I_len*1.04, 0.12, "I", color='magenta', fontsize=13, weight='bold')

# Кути
def draw_angle(radius, start_deg, end_deg, color, label, fsize=13, label_scale=1.02):
    arc = np.deg2rad(np.linspace(start_deg, end_deg, 120))
    ax.plot(radius*np.cos(arc), radius*np.sin(arc), color=color, lw=2)
    mid = np.deg2rad((start_deg+end_deg)/2)
    ax.text(label_scale*radius*np.cos(mid), label_scale*radius*np.sin(mid),
            label, color=color, fontsize=fsize)

draw_angle(radius=3.2, start_deg=0, end_deg=fiL,  color='blue',  label='φL', label_scale=1.02)
draw_angle(radius=3.0, start_deg=0, end_deg=-fiC, color='green', label='φC', label_scale=1.08)
draw_angle(radius=3.6, start_deg=0, end_deg=fi,  color='red',   label='φ',  label_scale=1.08)

# Оформлення
ax.axhline(0, color='gray', lw=0.9)
ax.axvline(0, color='gray', lw=0.9)
ax.set_xlabel("Дійсна вісь")
ax.set_ylabel("Уявна вісь")
ax.set_title("")
rad = max(UR, UL, UC, U)*1.55
ax.set_xlim(-rad, rad)
ax.set_ylim(-rad, rad)

ax.text(0.02, 0.98,
        f""
        f""
        f"",
        transform=ax.transAxes, va='top', fontsize=11)

plt.grid(True, alpha=0.6)
plt.tight_layout()
plt.show()