import math

U10 = 12.07
U1k = 12.30
U20 = 10.80
U2k = 10.60
I10 = 0.0345
I1k = 0.0390
I20 = 0.0490
I2k = 0.0540
P1 = 0.155
P2 = 0.48

phi10 = -68.14
phi1k = -75.51
phi20 = 24.90
phi2k = 11.95



Z10 = U10 / I10
Z1k  = U1k / I1k
Z20 = U20 / I20
Z2k  = U2k / I2k

print(f"Z10 = {Z10:.3f}e^(i * {phi10})")
print(f"Z1k  = {Z1k:.3f}e^(i * {phi1k})")
print(f"Z20 = {Z20:.3f}e^(i * {phi20})")
print(f"Z2k  = {Z2k:.3f}e^(i * {phi2k})")

Z1 = Z10 / Z1k
phi1 = phi10 - phi1k

Z2 = Z20 / Z2k
phi2 = phi20 - phi2k

print(f"Z1 = {Z1:.3f}e^(i * {phi1:.2f})")
print(f"Z2 = {Z2:.3f}e^(i * {phi2:.2f})")

Z10 = Z10 * complex(math.cos(math.radians(phi10)), math.sin(math.radians(phi10)))
Z1k  = Z1k  * complex(math.cos(math.radians(phi1k)),  math.sin(math.radians(phi1k)))
Z20 = Z20 * complex(math.cos(math.radians(phi20)), math.sin(math.radians(phi20)))
Z2k  = Z2k  * complex(math.cos(math.radians(phi2k)),  math.sin(math.radians(phi2k)))

D = (Z20 / (Z10 - Z1k))**(0.5)
C = D / Z20
A = Z10 * C
B = Z1k * D

print("Коефіцієнти ABCD:")
print(f"A = {A:.3f}")
print(f"B = {B:.3f}")
print(f"C = {C:.3f}")
print(f"D = {D:.3f}")

print(f"\nПеревірка умови AD - BC = 1: {A*D:.3f} - {B*C:.3f} = {(A*D - B*C):.3f}")

Y0 = C; R0 = 1 / C
Z1 = (A - 1) / C
Z2 = (D - 1) / C

print(f"\nY0 = {Y0:.3f} См = R0 = {R0:.3f} Ом")
print(f"Z1 = {Z1:.3f} Ом")
print(f"Z2 = {Z2:.3f} Ом")
