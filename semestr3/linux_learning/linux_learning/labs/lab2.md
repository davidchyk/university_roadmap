# ЛР №2 — команди для всіх варіантів

# 0) Підготовка файлів
cp /etc/passwd ~/lab2/pass.txt # копія passwd у домашній каталог

# ========== Варіанти ==========

# Варіант 1
```bash
cat test.txt city.txt pass.txt
wc -l test.txt city.txt pass.txt
cut -d: -f1,3 pass.txt
head -n 3 pass.txt
sort city.txt
sed 's/a/b/g' city.txt
grep "Spain" city.txt
split -l 3 city.txt part_
```

# Варіант 2
```bash
cat test.txt city.txt pass.txt
wc -w test.txt city.txt pass.txt
cut -c1-10 pass.txt
tail -n 3 pass.txt
sort -r city.txt
sed 's/in/ /g' city.txt
grep -v "Spain" city.txt
split -l 3 city.txt part_
```

# Варіант 3
```bash
cat test.txt city.txt pass.txt
wc -m test.txt city.txt pass.txt
cut -d: -f1 pass.txt
head -n 10 pass.txt
sort city.txt
sed 's/et/in/g' city.txt
grep -E "Hungary|Austria" city.txt
split -l 3 city.txt part_
```

# Варіант 4
```bash
cat test.txt city.txt pass.txt
wc -l test.txt city.txt pass.txt
cut -d: -f2 pass.txt
tail -n 8 pass.txt
sort -r city.txt
sed 's/et/ /g' city.txt
grep -Ev "Spain|Vienna" city.txt
split -l 3 city.txt part_
```

# Варіант 5
```bash
cat test.txt city.txt pass.txt
wc -w test.txt city.txt pass.txt
cut -c1-3 pass.txt
head -n 5 pass.txt
sort city.txt
sed 's/ /  /g' city.txt
grep -E "^Bu" city.txt
split -l 3 city.txt part_
```

# Варіант 6
```bash
cat test.txt city.txt pass.txt
wc -m test.txt city.txt pass.txt
cut -d: -f4 pass.txt
tail -n 6 pass.txt
sort -r city.txt
sed 's/,/:/g' city.txt
grep "Budapest" city.txt
split -l 3 city.txt part_
```

# Варіант 7
```bash
cat test.txt city.txt pass.txt
wc -l test.txt city.txt pass.txt
cut -d: --complement -f2 pass.txt
head -n 7 pass.txt
sort city.txt
sed 's/ /,/g' city.txt
grep -v "Budapest" city.txt
split -l 3 city.txt part_
```

# Варіант 8
```bash
cat test.txt city.txt pass.txt
wc -w test.txt city.txt pass.txt
cut -d: -f6,1 pass.txt
tail -n 8 pass.txt
sort -r city.txt
sed -e 's/a/X/g' -e 's/b/Y/g' -e 's/c/Z/g' city.txt
grep -E "Hungary|Austria" city.txt
split -l 3 city.txt part_
```

# Варіант 9
```bash
cat test.txt city.txt pass.txt
wc -m test.txt city.txt pass.txt
cut -d: -f1,3 pass.txt
head -n 9 pass.txt
sort city.txt
sed 's/,/,,/g' city.txt
grep -Ev "Spain|Vienna" city.txt
split -l 3 city.txt part_
```

# Варіант 10
```bash
cat test.txt city.txt pass.txt
wc -l test.txt city.txt pass.txt
cut -c2-5 pass.txt
tail -n 10 pass.txt
sort -r city.txt
sed 's/\?/\?!/g' city.txt
grep -E "^Bu" city.txt
split -l 3 city.txt part_
```

# Варіант 11
```bash
cat test.txt city.txt pass.txt
wc -w test.txt city.txt pass.txt
cut -d: --complement -f1 pass.txt
head -n 11 pass.txt
sort city.txt
sed -e 's/a/X/g' -e 's/b/Y/g' -e 's/c/\//g' city.txt
grep -i "austria" city.txt
split -l 3 city.txt part_
```

# Варіант 12
```bash
cat test.txt city.txt pass.txt
wc -m test.txt city.txt pass.txt
cut -d: -f6,7 pass.txt
head -n 12 pass.txt
sort -r city.txt
sed 's/[[:space:]]//g' city.txt
grep -E "^Au" city.txt
split -l 3 city.txt part_
```

# Варіант 13
```bash
cat test.txt city.txt pass.txt
wc -l test.txt city.txt pass.txt
cut -d: -f7,6 pass.txt
tail -n 13 pass.txt
sort city.txt
sed 's/,//g' city.txt
grep -Ev "^B" city.txt
split -l 3 city.txt part_
```

# Варіант 14
```bash
cat test.txt city.txt pass.txt
wc -w test.txt city.txt pass.txt
cut -c10-20 pass.txt
head -n 14 pass.txt
sort -r city.txt
sed 's/b/a/g' city.txt
grep -E '8$' city.txt
split -l 3 city.txt part_
```

# Варіант 15
```bash
cat test.txt city.txt pass.txt
wc -m test.txt city.txt pass.txt
cut -d: -f7 pass.txt
head -n 15 pass.txt
sort city.txt
sed 's/a/\//g' city.txt
grep "Munich" city.txt
split -l 3 city.txt part_
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