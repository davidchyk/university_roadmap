import cmath
import math

S, N, k = 1, 6, 1

j = 1j  # уявна одиниця

Z1 = (N * S) - j * (10 * N) * k          # Ом
Z2 = (N + S) + j * (10 * S) * k          # Ом
Z0 = 10 * S + N                          # Ом
U1 = 20                                  # В
U2 = 4 + S                               # В
f  = (10 * S) + (10 * N)               # Гц  (10^S + 10^N)

A = 1 + Z0 / Z2
B = Z0
C = 1/Z1 + 1/Z2 + Z0/(Z1*Z2)
D = 1 + Z0 / Z1

EQ = A*D - B*C

print(f"Z1 = {Z1:.3f} Ом")
print(f"Z2 = {Z2:.3f} Ом")
print(f"Z0 = {Z0:.3f} Ом")
print(f"U1 = {U1:.3f} В")
print(f"U2 = {U2:.3f} В")
print(f"f  = {f:.3f} Гц\n")

print(f"Параметри П-подібного чотириполюсника:")
print(f"A = {A:.3f}")
print(f"B = {B:.3f}")
print(f"C = {C:.3f}")
print(f"D = {D:.3f}\n")

print(f"Перевірка умови AD - BC = 1: {A*D:.3f} - {B*C:.3f} = {EQ:.3f}")

Y11 = D / B
Y12 = -1 / B
Y22 = A / B
Y21 = Y12

I1 = Y11 * U1 + Y12 * U2
I2 = -(Y21 * U1 + Y22 * U2)

absI1 = abs(I1)
absI2 = abs(I2)

phiI1 = math.degrees(cmath.phase(I1))
phiI2 = math.degrees(cmath.phase(I2))

print(f"I1 = {I1:.3f}, |I1| = {absI1:.3f}, arg(I1) = {phiI1:.2f}")
print(f"I2 = {I2:.3f}, |I2| = {absI2:.3f}, arg(I2) = {phiI2:.2f}")

Z_H = U2 / I2

print(f"Z_H = {Z_H:.3f} Ом")

omega = 2 * math.pi * f

C_1 = -1 / (omega * Z1.imag)
L_2 = Z2.imag / (omega)
C_H = -1 / (omega * Z_H.imag)

R_0 = Z0.real
R_1 = Z1.real
R_2 = Z2.real
R_H = Z_H.real

print(f"C_1 = {C_1*1e6:.3f} мкФ")
print(f"L_2 = {L_2*1e3:.3f} мГн")
print(f"C_H = {C_H*1e6:.3f} мкФ")
print(f"R_0 = {R_0:.3f} Ом")
print(f"R_1 = {R_1:.3f} Ом")
print(f"R_2 = {R_2:.3f} Ом")
print(f"R_H = {R_H:.3f} Ом")