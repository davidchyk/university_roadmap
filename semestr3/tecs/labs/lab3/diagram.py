import numpy as np
import math
import matplotlib.pyplot as plt

# твої RMS-значення
UR  = 9.513 - 0.422j
URL = 4.345 - 3.490j
UXL = 3.143 + 3.912j
URC = 0.060 + 0.912j
UC  = -7.427 + 0.491j      # задане «знизу вгору»
E   = 17 + 0j

# Currents (given):
I1 = 0.043 - 0.002j
I2 = 0.041 - 0.033j
I3 = 0.002 + 0.031j
I23 = I2 + I3  # should equal I1

def chain_points(vectors):
    """[0, z1, z1+z2, z1+z2+z3, ...]"""
    pts=[0+0j]; s=0+0j
    for z in vectors:
        s += z
        pts.append(s)
    return pts

def draw_chain_labeled(ax, vs, labels, color='C3', chain_label=None):
    pts = chain_points(vs)
    for i, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
        ax.annotate('', xy=(b.real, b.imag), xytext=(a.real, a.imag),
                    arrowprops=dict(arrowstyle='->', lw=1.8, color=color))
        if labels and i < len(labels) and labels[i]:
            mx = (a.real + b.real) / 2
            my = (a.imag + b.imag) / 2
            dx = b.real - a.real; dy = b.imag - a.imag
            ang = math.degrees(math.atan2(dy, dx))
            norm = math.hypot(dx, dy) or 1.0
            off = 0.15
            nx = -dy / norm; ny = dx / norm
            ax.text(mx + off*nx, my + off*ny, labels[i], color=color,
                    rotation=ang, rotation_mode='anchor',
                    ha='center', va='center')
    if chain_label:
        ax.text(pts[-1].real+0.1, pts[-1].imag+0.1, chain_label, color=color)
    return pts[-1]

def draw_chain(ax, vs, label, color='C3'):
    pts = chain_points(vs)
    # стрілки 'tip-to-tail'
    for a,b in zip(pts[:-1], pts[1:]):
        ax.annotate('', xy=(b.real,b.imag), xytext=(a.real,a.imag),
                    arrowprops=dict(arrowstyle='->', lw=1.8, color=color))
    ax.text(pts[-1].real+0.1, pts[-1].imag+0.1, label, color=color)
    return pts[-1]

fig, ax = plt.subplots(figsize=(8,5))
ax.set_aspect('equal', adjustable='datalim')
ax.grid(True, alpha=.3); ax.axhline(0); ax.axvline(0)

# Ліва гілка: U_R + U_RL + U_XL
tip_left  = draw_chain_labeled(ax, [UR, URL, UXL], labels=[r'$U_R$', r'$U_{RL}$', r'$U_{XL}$'], color='tab:red') # $U_R+U_{RL}+U_{XL}$

# Права гілка: U_R + U_RC - U_C   (увага на знак)
tip_right = draw_chain_labeled(ax, [UR, URC, -UC], labels=[r'$U_R$', r'$U_{RC}$', r'$U_C$'], color='tab:orange') # $U_R+U_{RC}-U_C$

# Currents phasors: chain I2 -> I3 and resultant I1
draw_chain_labeled(ax, [I2, I3], labels=[r'$I_2$', r'$I_3$'], color='tab:green')
draw_chain_labeled(ax, [I1], labels=[r'$I_1$'], color='tab:purple')

# Вектор Е від початку
ax.annotate('', xy=(E.real,E.imag), xytext=(0,0),
            arrowprops=dict(arrowstyle='->', lw=2.0, color='tab:blue'))
ax.text(E.real+0.1, E.imag+0.1, r'$E$', color='tab:blue')

# Перевірки у заголовку
def pol(z): return f"{abs(z):.3f} ∠ {math.degrees(math.atan2(z.imag,z.real)):.2f}°"
ax.set_title(
    rf"$U_R+U_{{RL}}+U_{{XL}} = {pol(tip_left)}$"+"\n"+
    rf"$U_R+U_{{RC}}-U_C = {pol(tip_right)}$"+"\n"+
    rf"$E = {pol(E)}$"+"\n"+
    rf"$I_2+I_3 = I_1 = {pol(I23)} = {pol(I1)}$"
)

ax.set_xlabel('Re{·}'); ax.set_ylabel('Im{·}')
plt.tight_layout(); plt.show()
