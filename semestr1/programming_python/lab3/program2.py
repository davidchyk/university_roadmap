while True:

    byte_array = bytearray(input("Введіть рядок: "), encoding="utf-8")
    i = 0

    while i < len(byte_array):

        if byte_array[i] == ord("*"):
            del byte_array[i]

        else:

            byte_array.insert(i+1, byte_array[i])
            i += 2

    print(f"Новий байтовий масив: {byte_array}")