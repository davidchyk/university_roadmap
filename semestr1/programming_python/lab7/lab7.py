import os, shutil, pickle, shelve, re
import lab5, lab6

letter = input("Введіть одну букву для пошуку слів: ")

# 1. Створення каталогу C:\lab7
os.makedirs(r"C:\lab7", exist_ok=True)

# 2. Створення підкаталогу C:\lab7\<Давидчук>
os.makedirs(r"C:\lab7\Давидчук", exist_ok=True)

# 3. Завантаження файлу 8.txt в підкаталог та дії з ним
shutil.copyfile(r"C:\Users\artem\OneDrive\Desktop\Important folder\University\Programming\Lab7\8.txt", r"C:\lab7\Давидчук\8.txt")

with open(r"C:\lab7\Давидчук\8.txt", "r", encoding="windows-1251") as file: text = file.read()

sentences = re.split(r'[.!?]', text)

with open(r"C:\lab7\Давидчук\81.txt", "w", encoding="utf-8") as file:
    for sentence in sorted(sentences, key=len, reverse=True): file.write(sentence.strip() + "\n")

words = re.findall(fr'\b[{letter}]\w*', text)

with open(r"C:\lab7\Давидчук\82.txt", "w", encoding="utf-8") as file:
    for word in words: file.write(word + "\n")

# 4. Збереження даних з лабораторної роботи №5 з використанням pickle

lab5_data = {
    "L": lab5.L,
    "V": lab5.V,
    "speed": lab5.speed,
    "db": lab5.db
}

with open(r"C:\lab5\lab5_data.pkl", "wb") as file: pickle.dump(lab5_data, file)

with open(r"C:\lab5\lab5_data.pkl", "rb") as file: pickle_data = pickle.load(file)
pickle_data["Lab7_letter"] = letter

with open(r"C:\lab5\updated_lab5_data.pkl", "wb") as file: pickle.dump(pickle_data, file)

# 5. Збереження даних з лабораторної роботи №6 з використанням shelve

lab6_data = {

    "result": lab6.result,
    "Planets": lab6.Planets,
    "planet_list": lab6.planet_list,
    "mercury": lab6.mercury,
    "venus": lab6.venus,
    "earth": lab6.earth,
    "mars": lab6.mars,
    "jupiter": lab6.jupiter,
    "saturn": lab6.saturn,
    "uranus": lab6.uranus,
    "neptune": lab6.neptune,
    "pluto": lab6.pluto
}

with shelve.open(r"C:\lab6\lab6_data.db") as shelf:

    for key in lab6_data: shelf[key] = lab6_data[key]

    shelf["Lab7_letter"] = letter
    shelf["planet_list"][0] = "Sun"
    del shelf["result"]

    print("\n" r"Дані з C:\lab6\lab6_data.db:")

    for key in shelf: print(f"{key}: {shelf[key]}")