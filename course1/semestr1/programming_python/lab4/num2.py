from random import uniform

minimum = 1

m = int(input('Введіть число рядків: '))
n = int(input('Введіть число стовпців: '))

matrix = [[round(uniform(-50, 50), 4) for j in range(n)] for i in range(m)]
print(f'Матриця {m} на {n}: {matrix}')

for string in matrix: minimum *= min(string)

print(f"Добуток мінімальних значень кожного рядка: {minimum}")