from sys import exit

class char16bit:

    # Так як в мові Java тип char представляє собою unsigned 16bit ціле число
    # значить значення мають бути в діапазоні [0; 65536]
    # Я вручну напишу клас, який матиме схожі властивості

    def __init__(self, value):

        # Логіка при переповнені значення з діапазону [0; 65536] -> 16bit число зі знаком:
        if value < 0 or value > 65536: value % 65536

        self.value = value

    def __le__(self, other):

        # Використовується при операції <=
        return self.value <= other

    def __add__(self, other):

        # Використовується при операції +
        return char16bit(self.value + other)

    def __truediv__(self, other):

        # Використовується при операції /
        return char16bit(self.value / other.value)

    def __float__(self):

        # Використовується при виведенні значення до float
        return self.value

    def __str__(self):

        # Реалізовано, для відповідності типу
        return chr(self.value)

class Sum:

    def __init__(self, a, b, n, m):

        # Перевіряємо, щоб нижні границі суми не були більшими за верхні:

        if a > n or b > m: print(f"Wrong input limits of the summation"); exit()

        self.a = a
        self.b = b
        self.n = n
        self.m = m

    def calculate_and_print(self):

        result = 0

        # Перетворюємо в конкретний числовий тип для обчислення
        # Типи індексів завжди мають бути типом char16bit:

        i = char16bit(self.a)
        j = char16bit(self.b)

        # Проводимо обчислення:

        while i <= self.n:

            while j <= self.m:

                try:

                    result += float((i / j) / (i + 2))

                except ZeroDivisionError:

                    # В разі ділення на нуль
                    return f"ZeroDivivsionError"

                j += 1

            i += 1
            j = char16bit(self.b)

        return result

sum_result = Sum(int(input("a: ")), int(input("b: ")), int(input("n: ")), int(input("m: "))) # Введення значень a, b, n, m
print(sum_result.calculate_and_print()) # Виводимо результат