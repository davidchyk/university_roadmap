while True:

    a = input("Введіть перший рядок: ")
    b = input("Введіть другий рядок: ")

    if len(a) == len(b):

        new_string = ""

        for i in range(len(a)):
            new_string += a[i] + b[i]

        print(f"Новий рядок: {new_string}")

    else:
        print("Рядки не є однакового розміру")