import tkinter as tk
from tkinter import messagebox

def quicksort(arr):

    if len(arr) <= 1: return arr

    pivot = arr[0][1]
    less = [x for x in arr[1:] if x[1] <= pivot]
    greater = [x for x in arr[1:] if x[1] > pivot]

    return quicksort(less) + [arr[0]] + quicksort(greater)

def binary_search(arr, target):

    result = []
    left, right = 0, len(arr) - 1

    while left <= right:
    
        mid = (left + right) // 2
        age = arr[mid][1]

        if age == target:

            i = mid
            while i >= 0 and arr[i][1] == target:
                result.append(arr[i])
                i -= 1
            i = mid + 1
            while i < len(arr) and arr[i][1] == target:
                result.append(arr[i])
                i += 1
            break

        elif age < target: left = mid + 1
        else: right = mid - 1

    return result

people = [
    ("Анна", 20), ("Ігор", 25), ("Оля", 20), ("Сергій", 30), ("Марія", 25),
    ("Петро", 18), ("Люда", 22), ("Василь", 30), ("Катя", 19), ("Максим", 20),
    ("Олексій", 24), ("Даша", 21), ("Яна", 23), ("Тарас", 30), ("Інна", 19),
    ("Микола", 25), ("Юля", 16), ("Ростик", 17), ("Олеся", 17), ("Богдан", 31),
    ("Олена", 35), ("Роман", 40), ("Артем", 18), ("Михайло", 19), ("Едуард", 7)
]

sorted_people = quicksort(people)

root = tk.Tk()
root.title("Вибір імен за віком")
root.resizable(False, False)

base_label = tk.Label(root, text="Базова множина (Ім'я - Вік):")
base_label.pack()

base_text = tk.Text(root, height=10, width=40)
for name, age in sorted_people:
    base_text.insert(tk.END, f"{name} - {age} років\n")
base_text.config(state=tk.DISABLED)
base_text.pack()

entry_label = tk.Label(root, text="Введіть потрібні віки через кому:")
entry_label.pack()

entry = tk.Entry(root, width=30)
entry.pack()

result_label = tk.Label(root, text="Підмножина імен:")
result_label.pack()

result_text = tk.Text(root, height=5, width=40)
result_text.config(state=tk.DISABLED)
result_text.pack()

def search():

    input_str = entry.get()

    try: target_ages = list(map(int, input_str.split(",")))

    except ValueError:
        messagebox.showerror("Помилка", "Введіть числа, розділені комами"); return

    names = []
    for age in target_ages:
        matches = binary_search(sorted_people, age)
        names.extend([name for name, _ in matches])

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    if names:
        for name in names: result_text.insert(tk.END, name + "\n")
    else: result_text.insert(tk.END, "Нічого не знайдено")

    result_text.config(state=tk.DISABLED)

button = tk.Button(root, text="Знайти імена", command=search)
button.pack(pady=5)

root.mainloop()