from __future__ import annotations

def radix_sort(arr: list[int]) -> tuple[list[int], int]:
    ops = 0

    ops += 1  # перевірка if not arr
    if not arr:
        ops += 1  # return
        return arr, ops

    max_num = max(arr)
    ops += len(arr)  # пошук максимуму = n операцій

    exp = 1
    ops += 1  # присвоєння

    ops += 1  # перша перевірка while
    while max_num // exp > 0:
        ops += 1  # обчислення max_num // exp > 0

        _, sub_ops = counting_sort_by_digit(arr, exp)
        ops += sub_ops

        exp *= 10
        ops += 1  # множення + присвоєння

        ops += 1  # наступна перевірка while

    ops += 1  # return
    return arr, ops

def counting_sort_by_digit(arr: list[int], exp: int) -> tuple[list[int], int]:
    ops = 0

    n = len(arr)
    ops += 1

    output = [0] * n
    ops += n  # створення масиву довжини n

    count = [0] * 10
    ops += 10  # створення масиву довжини 10

    # Підрахунок цифр
    for num in arr:
        ops += 1  # ітерація циклу
        digit = (num // exp) % 10
        ops += 2  # // і %
        count[digit] += 1
        ops += 1  # інкремент

    ops += 1  # завершальна перевірка циклу

    # Префіксні суми
    for i in range(1, 10):
        ops += 1  # ітерація циклу
        count[i] += count[i - 1]
        ops += 2  # індексація + додавання

    ops += 1  # завершальна перевірка циклу

    # Побудова output справа наліво
    for i in range(n - 1, -1, -1):
        ops += 1  # ітерація циклу
        digit = (arr[i] // exp) % 10
        ops += 3  # arr[i], //, %
        output[count[digit] - 1] = arr[i]
        ops += 3  # count[digit], -1, присвоєння
        count[digit] -= 1
        ops += 2  # доступ + декремент

    ops += 1  # завершальна перевірка циклу

    # Копіювання назад
    for i in range(n):
        ops += 1  # ітерація циклу
        arr[i] = output[i]
        ops += 2  # читання + присвоєння

    ops += 1  # завершальна перевірка циклу

    ops += 1  # return
    return arr, ops