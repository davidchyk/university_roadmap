import numpy as np

S, N = 1, 6

E1 = N*10
E2 = N*5
R1 = 50+N*S
R2 = 75+N*S
R3 = 120+N*S
R4 = 180+N*S
R5 = 200+N*S
R6 = 220+N*S

print(
    "E1 = ", E1, "В,",
    "E2 = ", E2, "В,",
    "R1 = ", R1, "Ом,",
    "R2 = ", R2, "Ом,",
    "R3 = ", R3, "Ом,",
    "R4 = ", R4, "Ом,",
    "R5 = ", R5, "Ом,",
    "R6 = ", R6, "Ом"
)

# невідомі: x = [I1, I2, I3, I4, I5, I6]
A = np.array([
    [R1, R2,   0,  0, 0, 0],   # I1*R1 + I2*R2 = E2
    [0,   0,   0,  R4, 0, R6],      # I4*R4 + I6*R6 = -E2
    [0,  -R2,  R3, -R4, 0, 0],       # -I2*R2 - I3*R3 + I4*R4 = -E1
    [-1,  0,   0,  0,  1, 1],       # I5 + I6 - I1 = 0
    [0,   0,   1,  1,  0, -1],      # I3 + I4 - I6 = 0
    [0,   1,   0, -1, -1, 0],       # I2 - I5 - I4 = 0
], dtype=float)
b = np.array([E2, -E2, E1, 0, 0, 0], dtype=float)

x = np.linalg.solve(A, b)
I1, I2, I3, I4, I5, I6 = x

phi1 = I1*R1
phi2 = E1 - I3*R3
phi3 = -I2*R2
phi4 = 0

U21 = phi2 - phi1
U13 = phi1 - phi3
U14 = phi1 - phi4
U32 = phi3 - phi2
U42 = phi4 - phi2
U43 = phi4 - phi3

P1 = I1*I1*R1
P2 = I2*I2*R2
P3 = I3*I3*R3
P4 = I4*I4*R4
P6 = I6*I6*R6

PE1 = E1*I3
PE2 = E2*I5

CONSUMER_POWER = P1 + P2 + P3 + P4 + P6
SOURCE_POWER = PE1 + PE2

print("Розраховані сили струму:")

print(f"I1 = {I1:.3f}, А")
print(f"I2 = {I2:.3f}, А")
print(f"I3 = {I3:.3f}, А")
print(f"I4 = {I4:.3f}, А")
print(f"I5 = {I5:.3f}, А")
print(f"I6 = {I6:.3f}, А\n")

print("Розраховані потенціали вузлів:")

print(f"phi1 = {phi1:.3f}, В")
print(f"phi2 = {phi2:.3f}, В")
print(f"phi3 = {phi3:.3f}, В")
print(f"phi3 = {phi4:.3f}, В\n")

print("Розраховані напруги віток:")

print(f"U21 = {U21:.3f}, В")
print(f"U13 = {U13:.3f}, В")
print(f"U14 = {U14:.3f}, В")
print(f"U32 = {U32:.3f}, В")
print(f"U42 = {U42:.3f}, В")
print(f"U43 = {U43:.3f}, В\n")

print("Розраховані потужності джерел та споживачів:")

print(f"Потужність споживачів = P1 + P2 + P4 + P6 = {P1:.3f} + {P2:.3f} + {P3:.3f} + {P4:.3f} + {P6:.3f} = {CONSUMER_POWER:.3f} Вт")
print(f"Потуржність джерел PE1 + PE2 = {PE1:.3f} + {PE2:.3f} = {SOURCE_POWER:.3f} Вт")