import math

S, N, k = 1, 6, 1

U_m = 10 + S
U_real = U_m / math.sqrt(2)
alpha = 90 - 2*N
f = S*100 + N
Z_H = (N+5+10*S) + 1.0j * (2*N+10*S)*k

omega = 2 * math.pi * f

print("Параметри схеми:\n")

print(f"U_m = {U_m}, В")
print(f"U_real = {U_real:.3f}, В")
print(f"alpha = {alpha}, град")
print(f"f = {f}, Гц")
print(f"Z_H = {Z_H}, Ом")

X_R = Z_H.real
X_L = Z_H.imag

L = X_L / omega

print(f"L = {L:.3f}")

T = 1/f

delta_T = 1.212e-3
phi = 360*delta_T / T

print(f"phi = {phi:.2f} град")