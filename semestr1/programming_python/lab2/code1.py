from math import sin, sqrt

x = float(input("Введіть значення x: ")) #приймаю значення x
y = float(input("Введіть значення y: ")) #приймаю значення y

print("R =", 2.37*sin(x+1)/sqrt(4*y**2 - 0.1*y + 5)) #розраховую значення R