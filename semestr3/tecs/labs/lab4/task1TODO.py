import math

U_R = 2.95
U_L = 5.60
U_C = 13.12
U_ALL = 10.40

P_R = 0.013
P_L = 0.14
P_C = 0.03
P_ALL = 0.27 #0.30

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

phi_R = math.degrees(math.acos(P_R / (U_R * I)))
phi_L = math.acos(P_L / (U_L * I))
phi_C = math.degrees(math.acos(P_C / (U_C * I)))
phi_ALL = math.acos(P_ALL / (U_ALL * I))

print("phi:")
print(f"phi_R = {phi_R}")
print(f"phi_L = {phi_L}")
print(f"phi_C = {phi_C}")
print(f"phi = {phi_ALL}")

R_R = P_R / I**2
R_L = P_L / I**2
R_C = P_C / I**2
R_ALL = P_R / I**2

print("R:")
print(f"R_R = {R_R}")
print(f"R_R = {R_R}")
print(f"R_R = {R_R}")
print(f"R = {R_ALL}")
