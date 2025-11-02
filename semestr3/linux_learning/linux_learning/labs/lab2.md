# ЛР №2 — команди для всіх варіантів

# 0) Підготовка файлів
cp /etc/passwd ~/lab2/pass.txt # копія passwd у домашній каталог

# ========== Варіанти ==========

# Варіант 1
```bash
cat test.txt city.txt pass.txt              # вивести вміст трьох файлів послідовно
wc -l test.txt city.txt pass.txt           # підрахувати кількість рядків у кожному файлі
cut -d: -f1,3 pass.txt                     # вирізати 1-ше і 3-тє поля (роздільник ':')
head -n 3 pass.txt                         # показати перші 3 рядки файлу
sort city.txt                              # відсортувати рядки у зростаючому порядку (ASCII/лексикографічно)
sed 's/a/b/g' city.txt                     # замінити всі 'a' на 'b' у кожному рядку
grep "Spain" city.txt                      # знайти рядки, що містять підрядок "Spain"
split -l 3 city.txt part_                  # розбити файл на частини по 3 рядки, імена починаються з 'part_'

```

# Варіант 2
```bash
cat test.txt city.txt pass.txt              # вивести вміст трьох файлів
wc -w test.txt city.txt pass.txt           # підрахувати кількість слів у кожному файлі
cut -c1-10 pass.txt                        # взяти лише символи з 1 по 10 у кожному рядку
tail -n 3 pass.txt                         # показати останні 3 рядки
sort -r city.txt                           # відсортувати у зворотному порядку (reverse)
sed 's/in/ /g' city.txt                    # замінити всі входження "in" на пробіл
grep -v "Spain" city.txt                   # показати рядки, що НЕ містять "Spain"
split -l 3 city.txt part_                  # розбити на файли по 3 рядки
```

# Варіант 3
```bash
cat test.txt city.txt pass.txt              # вивести вміст файлів
wc -m test.txt city.txt pass.txt           # підрахувати кількість символів (bytes/characters) у файлах
cut -d: -f1 pass.txt                       # взяти тільки перше поле (роздільник ':')
head -n 10 pass.txt                        # перші 10 рядків
sort city.txt                              # сортування за зростанням
sed 's/et/in/g' city.txt                   # замінити "et" на "in" всюди
grep -E "Hungary|Austria" city.txt         # рядки, де є "Hungary" АБО "Austria" (regex альтернація)
split -l 3 city.txt part_                  # по 3 рядки в частині
```

# Варіант 4
```bash
cat test.txt city.txt pass.txt              # вивести вміст файлів
wc -l test.txt city.txt pass.txt           # кількість рядків у кожному
cut -d: -f2 pass.txt                       # взяти друге поле (роздільник ':')
tail -n 8 pass.txt                         # останні 8 рядків
sort -r city.txt                           # сортування у зворотному порядку
sed 's/et/ /g' city.txt                    # замінити "et" на пробіл
grep -Ev "Spain|Vienna" city.txt           # показати рядки, що НЕ містять "Spain" і НЕ "Vienna" (розширений regex)
split -l 3 city.txt part_                  # розбити по 3 рядки
```

# Варіант 5
```bash
cat test.txt city.txt pass.txt              # вивести вміст файлів
wc -w test.txt city.txt pass.txt           # підрахунок слів
cut -c1-3 pass.txt                         # перші 3 символи кожного рядка
head -n 5 pass.txt                         # перші 5 рядків
sort city.txt                              # сортування зростаюче
sed 's/ /  /g' city.txt                    # замінити один пробіл на два (подвоїти пробіли)
grep -E "^Bu" city.txt                     # рядки, що починаються з "Bu" (якір початку рядка ^)
split -l 3 city.txt part_                  # розбити по 3 рядки
```

# Варіант 6
```bash
cat test.txt city.txt pass.txt              # вміст файлів
wc -m test.txt city.txt pass.txt           # кількість символів
cut -d: -f4 pass.txt                       # 4-те поле (роздільник ':')
tail -n 6 pass.txt                         # останні 6 рядків
sort -r city.txt                           # сортування у зворотному порядку
sed 's/,/:/g' city.txt                     # замінити коми на двокрапки
grep "Budapest" city.txt                   # рядки з "Budapest"
split -l 3 city.txt part_                  # розбити по 3 рядки
```

# Варіант 7
```bash
cat test.txt city.txt pass.txt              # вивести вміст
wc -l test.txt city.txt pass.txt           # кількість рядків
cut -d: --complement -f2 pass.txt          # взяти всі поля ОКРІМ 2-го (роздільник ':')
head -n 7 pass.txt                         # перші 7 рядків
sort city.txt                              # сортування зростаюче
sed 's/ /,/g' city.txt                     # замінити пробіли на коми
grep -v "Budapest" city.txt                # виключити рядки з "Budapest"
split -l 3 city.txt part_                  # розбити по 3 рядки
```

# Варіант 8
```bash
cat test.txt city.txt pass.txt                              # вивести вміст
wc -w test.txt city.txt pass.txt                           # підрахувати слова
cut -d: -f6,1 pass.txt                                     # взяти 6-те і 1-ше поля (у такому порядку)
tail -n 8 pass.txt                                         # останні 8 рядків
sort -r city.txt                                           # сортування у зворотному порядку
sed -e 's/a/X/g' -e 's/b/Y/g' -e 's/c/Z/g' city.txt        # послідовні багаторазові заміни a→X, b→Y, c→Z
grep -E "Hungary|Austria" city.txt                         # рядки з "Hungary" або "Austria"
split -l 3 city.txt part_                                  # розбити по 3 рядки
```

# Варіант 9
```bash
cat test.txt city.txt pass.txt              # вивести вміст
wc -m test.txt city.txt pass.txt           # кількість символів
cut -d: -f1,3 pass.txt                     # 1-ше і 3-тє поля (роздільник ':')
head -n 9 pass.txt                         # перші 9 рядків
sort city.txt                              # сортування зростаюче
sed 's/,/,,/g' city.txt                    # замінити ',' на подвійні ',,'
grep -Ev "Spain|Vienna" city.txt           # виключити рядки з "Spain" або "Vienna"
split -l 3 city.txt part_                  # розбити по 3 рядки
```

# Варіант 10
```bash
cat test.txt city.txt pass.txt              # вивести вміст
wc -l test.txt city.txt pass.txt           # кількість рядків
cut -c2-5 pass.txt                         # символи з 2 по 5 включно
tail -n 10 pass.txt                        # останні 10 рядків
sort -r city.txt                           # сортування у зворотному порядку
sed 's/\?/\?!/g' city.txt                  # замінити '?' на '?!' (екранування '?' у regex)
grep -E "^Bu" city.txt                     # рядки, що починаються з "Bu"
split -l 3 city.txt part_                  # розбити по 3 рядки
```

# Варіант 11
```bash
cat test.txt city.txt pass.txt                             # вивести вміст
wc -w test.txt city.txt pass.txt                          # кількість слів
cut -d: --complement -f1 pass.txt                         # взяти всі поля, крім 1-го (роздільник ':')
head -n 11 pass.txt                                       # перші 11 рядків
sort city.txt                                             # сортування зростаюче
sed -e 's/a/X/g' -e 's/b/Y/g' -e 's/c/\//g' city.txt      # заміни a→X, b→Y, c→/ (екранування '/')
grep -i "austria" city.txt                                # пошук "austria" без урахування регістру
split -l 3 city.txt part_                                 # розбити по 3 рядки
```

# Варіант 12
```bash
cat test.txt city.txt pass.txt              # вивести вміст
wc -m test.txt city.txt pass.txt           # кількість символів
cut -d: -f6,7 pass.txt                     # 6-те та 7-ме поля (роздільник ':')
head -n 12 pass.txt                        # перші 12 рядків
sort -r city.txt                           # сортування у зворотному порядку
sed 's/[[:space:]]//g' city.txt            # прибрати всі пробільні символи (пробіли, таби тощо)
grep -E "^Au" city.txt                     # рядки, що починаються з "Au"
split -l 3 city.txt part_                  # розбити по 3 рядки
```

# Варіант 13
```bash
cat test.txt city.txt pass.txt              # вивести вміст
wc -l test.txt city.txt pass.txt           # кількість рядків
cut -d: -f7,6 pass.txt                     # 7-ме та 6-те поля (у вказаному порядку)
tail -n 13 pass.txt                        # останні 13 рядків
sort city.txt                              # сортування зростаюче
sed 's/,//g' city.txt                      # видалити всі коми
grep -Ev "^B" city.txt                     # показати рядки, що НЕ починаються з 'B'
split -l 3 city.txt part_                  # розбити по 3 рядки
```

# Варіант 14
```bash
cat test.txt city.txt pass.txt              # вивести вміст
wc -w test.txt city.txt pass.txt           # кількість слів
cut -c10-20 pass.txt                       # символи з 10 по 20 включно
head -n 14 pass.txt                        # перші 14 рядків
sort -r city.txt                           # сортування у зворотному порядку
sed 's/b/a/g' city.txt                     # замінити всі 'b' на 'a'
grep -E '8$' city.txt                      # рядки, що закінчуються на '8' (якір кінця $)
split -l 3 city.txt part_                  # розбити по 3 рядки
```

# Варіант 15
```bash
cat test.txt city.txt pass.txt              # вивести вміст
wc -m test.txt city.txt pass.txt           # кількість символів
cut -d: -f7 pass.txt                       # 7-ме поле (роздільник ':')
head -n 15 pass.txt                        # перші 15 рядків
sort city.txt                              # сортування зростаюче
sed 's/a/\//g' city.txt                    # замінити 'a' на символ '/' (екранування '/')
grep "Munich" city.txt                     # рядки, що містять "Munich"
split -l 3 city.txt part_                  # розбити по 3 рядки
```

---

# Команди та їх опис

## Підготовка
- `cp /etc/passwd ~/lab2/pass.txt`  
  Копіює системний файл `passwd` у домашній каталог як `pass.txt`.

---

## Базові команди
- `cat file1 file2 ...`  
  Виводить вміст файлів послідовно у стандартний потік.

- `wc file...` — підрахунки:  
  - `-l` — кількість рядків  
  - `-w` — кількість слів  
  - `-m` — кількість символів  

- `head -n N file`  
  Виводить перші `N` рядків файлу.

- `tail -n N file`  
  Виводить останні `N` рядків файлу.

- `sort file`  
  Лексикографічне сортування рядків у зростаючому порядку.  
  - `-r` — у зворотному порядку (за спаданням).

- `split -l N file prefix_`  
  Розбиває файл на частини по `N` рядків. Файли отримують імена `prefix_aa`, `prefix_ab`, ...

---

## Витяг полів і символів
- `cut -d: -fLIST pass.txt` — вибирає поля за роздільником `:`:
  - `-f1` — логін користувача  
  - `-f2` — пароль/плейсхолдер  
  - `-f3` — UID  
  - `-f4` — GID  
  - `-f6` — домашній каталог  
  - `-f7` — shell  
  - `-f1,3`, `-f6,1`, `-f7,6` — кілька полів у вказаному порядку  
  - `--complement -fK` — усе, крім вказаного поля K  

- `cut -cA-B pass.txt` — вибирає діапазон символів у кожному рядку:
  - `-c1-10` — символи 1..10  
  - `-c2-5` — символи 2..5  
  - `-c10-20` — символи 10..20  

---

## Пошук рядків (grep)
- `grep "pattern" file`  
  Показує рядки, що містять вказаний шаблон.

Опції:
- `-v` — показати рядки, що **не** збігаються.  
- `-i` — нечутливість до регістру.  
- `-E` — розширені регулярні вирази (можна `|`, `+`, `?`, без екранування дужок).

Приклади:
- `"Spain"` — знаходить усі рядки з підрядком `Spain`.  
- `-E "Hungary|Austria"` — рядки з `Hungary` або `Austria`.  
- `-E "^Bu"` — рядки, що починаються з `Bu`.  
- `-E "8$"` — рядки, що закінчуються на `8`.  
- `-Ev "Spain|Vienna"` — виключає рядки з `Spain` або `Vienna`.  
- `-i "austria"` — знаходить `Austria` у будь-якому регістрі.  

---

## Редагування рядків (sed)
Форма: `sed 's/ШУКАТИ/ЗАМІНИТИ/g' file` — глобальна заміна.

Приклади:
- `'s/a/b/g'` — замінює `a` на `b`.  
- `'s/in/ /g'` — `in` → пробіл.  
- `'s/et/in/g'` — `et` → `in`.  
- `'s/et/ /g'` — `et` → пробіл.  
- `'s/ /,/g'` — пробіли → коми.  
- `'s/,/:/g'` — коми → двокрапки.  
- `'s/,/,,/g'` — одна кома → подвійна кома.  
- `'s/ /  /g'` — один пробіл → два пробіли.  
- `'s/\?/\?!/g'` — `?` → `?!`.  
- `'s/a/\//g'` — `a` → символ `/`.  
- `-e 's/a/X/g' -e 's/b/Y/g' -e 's/c/Z/g'` — кілька замін в одному запуску.  
- `-e 's/a/X/g' -e 's/b/Y/g' -e 's/c/\//g'` — `a` → `X`, `b` → `Y`, `c` → `/`.  
- `'s/[[:space:]]//g'` — видаляє усі пробільні символи (пробіли, табуляції, переноси рядків).  