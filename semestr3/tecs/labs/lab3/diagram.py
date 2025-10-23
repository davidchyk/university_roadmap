import math
import matplotlib.pyplot as plt

# ---------- дані (RMS-комплекси) ----------
UR  = 9.513 - 0.422j
URL = 4.345 - 3.490j
UXL = 3.143 + 3.912j
URC = 0.060 + 0.912j
UC  = -7.427 + 0.491j
E   = 17 + 0j

I1 = 0.043 - 0.002j
I2 = 0.041 - 0.033j
I3 = 0.002 + 0.031j
I23 = I2 + I3  # має дорівнювати I1

# ---------- утиліти ----------
def chain_points(vectors):
    """Повертає послідовність вершин ланцюжка: [0, z1, z1+z2, ...]."""
    pts = [0+0j]; s = 0+0j
    for z in vectors:
        s += z; pts.append(s)
    return pts

def draw_chain_labeled(ax, vs, labels, color='C3'):
    """Малює ланцюжок векторів 'tip-to-tail' з підписами на сегментах."""
    pts = chain_points(vs)
    for i, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
        ax.annotate('', xy=(b.real, b.imag), xytext=(a.real, a.imag),
                    arrowprops=dict(arrowstyle='->', lw=1.8, color=color))
        if labels and i < len(labels) and labels[i]:
            mx = (a.real + b.real)/2
            my = (a.imag + b.imag)/2
            dx, dy = b.real - a.real, b.imag - a.imag
            ang = math.degrees(math.atan2(dy, dx))
            norm = math.hypot(dx, dy) or 1.0
            off = 0.15
            # невеликий зсув перпендикулярно до сегмента
            ax.text(mx - off*dy/norm, my + off*dx/norm, labels[i],
                    color=color, rotation=ang, rotation_mode='anchor',
                    ha='center', va='center')
    return pts[-1]

def pol(z): 
    return f"{abs(z):.3f} ∠ {math.degrees(math.atan2(z.imag, z.real)):.2f}°"

# ---------- масштаб для струмів ----------
V_refs = [E, UR, URL, UXL, URC, UC]
I_refs = [I1, I2, I3, I23]
V_max = max(abs(z) for z in V_refs) or 1.0
I_max = max(abs(z) for z in I_refs) or 1.0
S_I = 0.30 * V_max / I_max   # найбільший струм ~30% довжини найбільшої напруги
# S_I = 100  # <- за потреби можна зафіксувати свій масштаб

# ---------- малювання ----------
fig, ax = plt.subplots(figsize=(10,5.5))
ax.set_aspect('equal', adjustable='datalim')
ax.grid(True, alpha=.3)
ax.axhline(0, color='0.25', lw=1)
ax.axvline(0, color='0.25', lw=1)
ax.set_xlabel('Re{·}')
ax.set_ylabel('Im{·}')

# Напруги (два ланцюжки та джерело E)
tip_left  = draw_chain_labeled(ax, [UR, URL, UXL],
                               labels=[r'$U_R$', r'$U_{RL}$', r'$U_{XL}$'],
                               color='tab:red')
tip_right = draw_chain_labeled(ax, [UR, URC, -UC],
                               labels=[r'$U_R$', r'$U_{RC}$', r'$U_C$'],
                               color='tab:orange')
ax.annotate('', xy=(E.real, E.imag), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', lw=2.0, color='tab:blue'))
ax.text(E.real*1.005+0.1, E.imag*1.005+0.1, r'$E$', color='tab:blue')

# Струми як ланцюжок: I2 -> I3 (масштабовані), і окремо I1 до тієї ж точки
end_I23 = draw_chain_labeled(ax, [I2*S_I, I3*S_I],
                             labels=[r'$I_2$', r'$I_3$'],
                             color='tab:green')
I1s = I1 * S_I
ax.annotate('', xy=(I1s.real, I1s.imag), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', lw=1.8, color='tab:purple'))
ax.text(I1s.real*1.02, I1s.imag*1.02, r'$I_1$', color='tab:purple',
        ha='left', va='bottom')

# Заголовок з перевірками і приміткою про масштаб струмів
ax.set_title(
    rf"$U_R+U_{{RL}}+U_{{XL}} = {pol(tip_left)}$"+"\n"+
    rf"$U_R+U_{{RC}}-U_C = {pol(tip_right)}$"+"\n"+
    rf"$I_2+I_3 = I_1 = {pol(I23)} = {pol(I1)}$"+"\n"
)

plt.tight_layout()
plt.show()
