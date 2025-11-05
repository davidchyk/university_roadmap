import math

U_R = 2.95
U_L = 5.60
U_C = 3.12
U_ALL = 10.40

P_R = 0.13
P_L = 0.14
P_C = 0.03
P_ALL = 0.30

I = 0.04

Z_R = U_R / I
Z_L = U_L / I
Z_C = U_C / I
Z_ALL = U_ALL / I

print("Z:")
print(f"Z_R: {Z_R}")
print(f"Z_L: {Z_L}")
print(f"Z_C: {Z_C}")
print(f"Z: {Z_ALL}\n")

try:

    phi_R = math.degrees(math.acos(P_R / (U_R * I)))

except:

    phi_R = 0

phi_L = math.degrees(math.acos(P_L / (U_L * I)))
phi_C = math.degrees(math.acos(P_C / (U_C * I)))
phi_ALL = math.degrees(math.acos(P_ALL / (U_ALL * I)))

print("phi:")
print(f"phi_R = {phi_R}")
print(f"phi_L = {phi_L}")
print(f"phi_C = {phi_C}")
print(f"phi = {phi_ALL}\n")

R_R = P_R / I**2
R_L = P_L / I**2
R_C = P_C / I**2
R_ALL = P_ALL / I**2

print("R:")
print(f"R_R = {R_R}")
print(f"R_L = {R_L}")
print(f"R_C = {R_C}")
print(f"R = {R_ALL:.3f}\n")

try:
    X_R = math.sqrt(Z_R**2 - R_R**2)
except:

    X_R = 0

X_L = math.sqrt(Z_L**2 - R_L**2)
X_C = -math.sqrt(Z_C**2 - R_C**2)
X_ALL = math.sqrt(Z_ALL**2 - R_ALL**2)

print("X:")
print(f"X_R = {X_R:.2f}")
print(f"X_L = {X_L:.2f}")
print(f"X_C = {X_C:.2f}")
print(f"X = {X_ALL:.2f}")

other_phiR = math.degrees(math.atan(X_R/R_R))
other_phiL = math.degrees(math.atan(X_L/R_C))
other_phiC = math.degrees(math.atan(X_C/R_C))
other_phiALL = math.degrees(math.atan(X_ALL/R_ALL))

print("otherPhi:")
print(f"phi R = {phi_R}")
print(f"phi L = {phi_L}")
print(f"phi C = {phi_C}")
print(f"phi ALL = {phi_ALL}")