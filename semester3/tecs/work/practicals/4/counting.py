import math

U_m = 28.284 # Вольт
phi = 60 # градусів
Z2 = 5 - 60j # 1 імпеданс: R = 5, X_C = -60
Z3 = 10 + 40j # 2 імпеданс: R = 10, X_L = 40
f = 100

# Constants:

omega = 2 * math.pi * f
period = 1/f
phi_rad = math.radians(phi)
x = round(math.cos(phi_rad), 3)
y = round(math.sin(phi_rad), 3)

U = U_m * (x + 1j * y)

I2 = U / Z2
I3 = U / Z3

print(I2)
print(I3)

moduleI2 = abs(I2)
moduleI3 = abs(I3)



print(U)