# ЛР №3 — Стандартні потоки, конвеєри, перенаправлення (усі варіанти)
# Підготовка (як у ЛР2)
#   - у робочому каталозі мають бути: test.txt, pass.txt (копія /etc/passwd), city.txt
#   - створюємо/очищуємо newfile.txt у кожному варіанті

# ========================= ВАРІАНТ 1 =========================
```bash
: > newfile.txt                                 # створити/очистити файл (нульова довжина)
grep -E '\b[BRS][[:alpha:]]*[an]\b' city.txt | wc -l > newfile.txt
                                                # порахувати рядки, де слово починається на B/R/S,
                                                # далі йдуть літери, і закінчується на a або n; записати кількість у newfile.txt
sort -r city.txt | grep -E '[68]$' >> newfile.txt
                                                # відсортувати у зворотному порядку і додати рядки, що закінчуються на 6 або 8, у кінець newfile.txt
cat newfile.txt                                 # показати вміст newfile.txt
ls > result.txt 2> error.txt                    # stdout ls у result.txt, stderr у error.txt
# F1 (root): bash-користувачі → їх $HOME (поле 6) → ls вмісту
sudo awk -F: '/\/bin\/bash/{print $6}' /etc/passwd | xargs -I {} ls {}
                                                # (root) взяти домашні каталоги bash-користувачів і виконати ls для кожного
```

# ========================= ВАРІАНТ 2 =========================
```bash
: > newfile.txt                                 # створити/очистити файл
grep -E '\b[1][0-9]*[68]\b' city.txt | wc -l > newfile.txt
                                                # порахувати слова-числа, що починаються з 1, далі 0–9, і закінчуються на 6 або 8
sort -u city.txt >> newfile.txt                 # унікальне сортування; додати до newfile.txt
cat newfile.txt                                 # показати результат
cdls > result.txt 2>&1                          # навмисно НЕіснуюча команда; і stdout, і stderr у result.txt
# F2 (user): /etc → *.conf та кількість рядків
cd /etc && ls *.conf | xargs wc -l              # перейти в /etc, перелік *.conf, підрахувати рядки у кожному
```

# ========================= ВАРІАНТ 3 =========================
```bash
: > newfile.txt                                 # створити/очистити
grep -i 'austria' city.txt | wc -l > newfile.txt
                                                # нечутливо до регістру знайти "austria" і порахувати кількість збігів
sort city.txt | uniq -d >> newfile.txt          # додати рядки, які зустрічаються більше одного разу (дублі)
cat newfile.txt                                 # показати
pwd > result.txt                                # записати поточний каталог у result.txt (stderr піде на екран)
# F3 (user): те саме, що F2
cd /etc && ls *.conf | xargs wc -l              # вивести кількість рядків по *.conf
```

# ========================= ВАРІАНТ 4 =========================
```bash
: > newfile.txt                                 # створити/очистити
grep -v 'Hungary' city.txt | wc -l > newfile.txt
                                                # порахувати рядки, що НЕ містять "Hungary"
sort city.txt | grep -E '^Be' >> newfile.txt    # додати рядки, що починаються з "Be"
cat newfile.txt                                 # показати
pwpd 2> error.txt                               # навмисно НЕіснуюча команда; stderr у error.txt, stdout на екран
# F4 (user): створити 111/222/333 і показати рядки, що містять ім’я файла; помилки у error.txt
cd ~
echo 111 > 111                                  # створити файл "111" з вмістом 111
echo 222 > yyy                                  # створити yyy з вмістом 222
echo 333 > 33343                                # створити 33343 з вмістом 333
for f in 111 222 333; do grep -Hn "$f" "$f"; done 2> error.txt
                                                # для 111 і 333 grep спрацює; для 222 файла немає → помилка в error.txt
```

# ========================= ВАРІАНТ 5 =========================
```bash
: > newfile.txt
grep 'Spain' city.txt | wc -l > newfile.txt     # кількість рядків із "Spain"
sort city.txt | grep -E '^Be' >> newfile.txt    # додати рядки на "Be"
cat newfile.txt
lasts 2> error.txt                              # навмисно НЕіснуюча команда; stderr у error.txt
# F5 (user): у ~ у файлах [a-z]*.txt показати рядки з 'root'
cd ~ && grep -Hn 'root' [a-z]*.txt              # шукає 'root' у текстових файлах з назвами a..z*.txt
```

# ========================= ВАРІАНТ 6 =========================
```bash
: > newfile.txt
grep -E '^[BM].*[678]$' city.txt | wc -l > newfile.txt
                                                # слова/рядки, що починаються на B або M і закінчуються на 6/7/8
sort city.txt | grep -E '6$'>> newfile.txt      # додати рядки, що закінчуються на 6
cat newfile.txt
ps > result.txt                                 # список процесів у result.txt (stderr на екран)
# F6 (user): filelist.txt → вивести кожен файл, у потоці замінити A на ім’я файла; помилки у error.txt
cd ~
nano filelist.txt                               # вручну створити файл зі списком імен (напр., pass.txt, city.txt, file123.txt)
xargs -I {} sh -c 'sed "s/A/{}/g" "{}"' < filelist.txt 2> error.txt
                                                # для кожного імені виконати sed: замінити 'A' на ім’я файла; помилки у error.txt
```

# ========================= ВАРІАНТ 7 =========================
```bash
: > newfile.txt
grep -E '\b[[:alpha:]]{5}\b' city.txt | wc -l > newfile.txt
                                                # кількість слів рівно з 5 букв
sort -r city.txt | grep -E '6$' >> newfile.txt  # додати рядки на '6' після реверс-сорту
cat newfile.txt
sp > result.txt 2>&1                            # навмисно НЕіснуюча команда; і stdout, і stderr у result.txt
# F7 (user): для кожного елемента з ls у /home — знайти збіг у /etc/passwd
for p in /home/*; do grep "$p" /etc/passwd; done
                                                # шукає шляхи /home/... у passwd (може не збігатися буквально)
```

# ========================= ВАРІАНТ 8 =========================
```bash
: > newfile.txt
grep -Ev '\b[[:alpha:]]{5}\b' city.txt | wc -l > newfile.txt
                                                # порахувати рядки/слова, де НЕ трапляються рівно 5-буквені слова
sort city.txt | grep -E '^Ba' >> newfile.txt    # додати рядки, що починаються на "Ba"
cat newfile.txt
ls > result.txt                                 # stdout у result.txt (stderr на екран)
# F8 (user): для кожного shell з /etc/shells (не коментар) знайти рядки у /etc/passwd
grep -v '^\s*#' /etc/shells | xargs -I {} grep {} /etc/passwd
                                                # пропустити коментарі і шукати shell у passwd
```

# ========================= ВАРІАНТ 9 =========================
```bash
: > newfile.txt
grep -E '\b[[:alpha:]]{6}\b' city.txt | wc -l > newfile.txt
                                                # порахувати 6-буквені слова
sort -u city.txt | grep -Ev 'Hungary|Spain' >> newfile.txt
                                                # унікальні рядки, виключити ті, що містять Hungary або Spain
cat newfile.txt
id > result.txt 2>&1                            # виконати id; і stdout, і stderr у result.txt
# F9 (root): bash-користувачі → імена → чи юзали sudo у /var/log/auth.log
sudo awk -F: '/\/bin\/bash/{print $1}' /etc/passwd | \
  while read u; do sudo grep -E "sudo.*$u" /var/log/auth.log; done
                                                # (root) для кожного bash-користувача шукати згадки про sudo у журналі
```

# ========================= ВАРІАНТ 10 =========================
```bash
: > newfile.txt
grep -Ev '\b[[:alpha:]]{6}\b' city.txt | wc -l > newfile.txt
                                                # порахувати рядки/слова без 6-буквених слів (заперечення)
sort city.txt | uniq -D >> newfile.txt          # додати лише дублікати (uniq -D показує всі повтори)
cat newfile.txt
ids > result.txt 2> error.txt                   # навмисно НЕіснуюча команда; stdout у result.txt, stderr у error.txt
# F10 (user): унікальні рядки city.txt, що не починаються на B → створити <поле1>.text
awk '!/^B/{print $1}' city.txt | sort -u | xargs -I {} sh -c 'echo {} > {}.text'
                                                # з першого поля згенерувати файли "<значення>.text"
```

# ========================= ВАРІАНТ 11 =========================
```bash
: > newfile.txt
grep -E '\b[[:alpha:]]{6}\b' city.txt | grep -Ev '\b[[:alpha:]]{8}\b' | wc -l > newfile.txt
                                                # порахувати 6-буквені, але без 8-буквених у тому самому рядку
sort city.txt | grep -E '^Be' >> newfile.txt    # додати рядки на "Be"
cat newfile.txt
lsmid 2> result.txt                             # навмисно НЕіснуюча команда; її stderr піде у result.txt
# F11 (user): PATH → каталоги → показати файли; помилки у error.txt
echo "$PATH" | tr ':' '\n' | xargs -I {} ls {} 2> error.txt
                                                # розбити PATH і виконати ls по кожному каталогу; помилки у error.txt
```

# ========================= ВАРІАНТ 12 =========================
```bash
: > newfile.txt
grep -E '\b[[:alpha:]]{6}\b' city.txt | grep -E '\b[[:alpha:]]{8}\b' | wc -l > newfile.txt
                                                # порахувати рядки, де трапляються і 6-, і 8-буквені слова
sort -u city.txt >> newfile.txt                 # додати унікальні рядки
cat newfile.txt
dirs > result.txt 2>&1                          # навмисно НЕіснуюча команда; все у result.txt
# F12 (root): /etc/passwd з /home/ і /bin/bash → імена → показати /home/<name>/.bash_history
sudo awk -F: '/\/home\// && /\/bin\/bash/{print $1}' /etc/passwd | \
  xargs -I {} sudo cat /home/{}/.bash_history   # (root) показати історію bash для користувачів із домашнім каталогом
```

# ========================= ВАРІАНТ 13 =========================
```bash
: > newfile.txt
grep -Ev "Spain|Vienna" city.txt | wc -l > newfile.txt
                                                # порахувати рядки без Spain і без Vienna
sort city.txt | uniq -d >> newfile.txt          # додати рядки, що дублюються
cat newfile.txt
ls 2> error.txt                                 # вивести список; помилки (якщо будуть) у error.txt
# F13 (root): bash-користувачі → виконати id для кожного
sudo awk -F: '/\/bin\/bash/{print $1}' /etc/passwd | xargs -I {} sudo id {}
                                                # (root) показати UID/GID/групи для кожного bash-користувача
```

# ========================= ВАРІАНТ 14 =========================
```bash
: > newfile.txt
sort -u city.txt | grep -E '[357]$' | wc -l > newfile.txt
                                                # порахувати унікальні рядки, що закінчуються на 3/5/7
sort city.txt | uniq -D >> newfile.txt          # додати рядки, що мають дублікати
cat newfile.txt
greb > result.txt 2>&1                          # навмисно НЕіснуюча команда; все у result.txt
# F14 (user): 2-ге поле city.txt → унікальні → відсортувати → взяти 3 → вивести <значення>.text; помилки у error.txt
awk '{print $2}' city.txt | sort -u | head -3 | xargs -I {} sh -c 'cat {}.text' 2> error.txt
                                                # взяти 3 унікальні значення з 2-го поля і показати відповідні файли *.text
```

# ========================= ВАРІАНТ 15 =========================
```bash
: > newfile.txt
grep -E '\b[[:alpha:]]*y\b' city.txt | wc -l > newfile.txt
                                                # порахувати слова, що закінчуються на 'y'
sort -r city.txt | grep -E '8$'                 >> newfile.txt
                                                # додати рядки, що закінчуються на 8, після реверс-сорту
cat newfile.txt
lsmod > result.txt                               # вивести модулі ядра; stdout у result.txt (stderr на екран)
# F15 (user): файл зі списком користувачів → виконати id для кожного; помилки у error.txt
# (вихідний файл повинен містити рядки: user, root, test, nobody, daemon, man)
xargs -I {} id {} < users.txt 2> error.txt       # для кожного імені з users.txt виконати 'id'; помилки у error.txt
```

---

# Команди та їх опис (ЛР №3)

## Підготовка
- `: > newfile.txt`  
  Створює порожній файл `newfile.txt` або очищує його (тривіальний запис у файл нічого).

---

## Робота з grep
- `grep -E 'REGEX' file`  
  Пошук рядків за розширеним регулярним виразом (ERE).  
  - `-i` — нечутливість до регістру.  
  - `-v` — інверсія (виводить рядки, що **не** відповідають).  
  - `-E` — увімкнення розширених регулярних виразів (дужки, |, + тощо).  

Приклади:
- `\b[BRS][[:alpha:]]*[an]\b` — слова, що починаються з B/R/S, містять літери, закінчуються на `a` або `n`.  
- `[68]$` — рядки, що закінчуються на 6 або 8.  
- `\b[1][0-9]*[68]\b` — числа, що починаються з `1`, далі цифри, закінчуються на 6 або 8.  
- `-i 'austria'` — слово `austria` у будь-якому регістрі.  
- `-v 'Hungary'` — усі рядки без `Hungary`.  
- `\b[[:alpha:]]{5}\b` — слова з рівно 5 букв.  
- `\b[[:alpha:]]{6}\b` — слова з 6 букв.  
- `\b[[:alpha:]]{8}\b` — слова з 8 букв.  
- `\b[[:alpha:]]*y\b` — слова, що закінчуються на `y`.  
- `-E "^Be"` — рядки, що починаються з `Be`.  
- `-Ev "Spain|Vienna"` — виключити рядки, де є Spain або Vienna.  

---

## Лічильники та сортування
- `wc -l` — підрахунок рядків.  
- `sort file` — сортування рядків.  
  - `-r` — зворотний порядок.  
  - `-u` — унікальні рядки.  
- `uniq -d` — повторювані рядки (дублі).  
- `uniq -D` — усі рядки, що дублюються (з повторами).  

---

## Перегляд і перенаправлення
- `cat file` — виводить файл.  
- `> file` — перенаправлення stdout у файл (перезапис).  
- `>> file` — дозапис у файл.  
- `2> file` — перенаправлення stderr у файл.  
- `2>&1` — об’єднання stderr зі stdout.  

---

## Службові команди (спеціально/помилково)
- `ls` — список файлів у каталозі.  
- `pwd` — поточний каталог.  
- `ps` — список процесів.  
- `id` — інформація про користувача.  
- `echo TEXT` — друк тексту.  
- `nano file` — редагування файлу.  
- `cd DIR` — змінити каталог.  

Некоректні (навмисно для демонстрації stderr → result.txt/error.txt):
- `cdls`, `pwpd`, `lasts`, `sp`, `ids`, `lsmid`, `dirs`, `greb`, `lsmod`  

---

## Робота з awk, xargs та циклами
- `awk -F: 'умова{дія}' file`  
  Обробка тексту з роздільником `:`.  
  - `/\/bin\/bash/{print $6}` — знайти рядки з `/bin/bash`, вивести 6-те поле (HOME).  
  - `/\/bin\/bash/{print $1}` — імена користувачів з bash.  
  - `/\/home\// && /\/bin\/bash/{print $1}` — користувачі з домашнім каталогом і bash.  
  - `!/^B/{print $1}` — перше поле рядків, що **не** починаються на B.  
  - `{print $2}` — друге поле (наприклад, назва міста).  

- `xargs` — запуск команд із аргументами, що беруться з stdin.  
  - `-I {}` — підстановка місця.  
  - `xargs -I {} ls {}` — для кожного аргументу виконати `ls`.  
  - `xargs wc -l` — порахувати рядки у кожному файлі.  

- Конвеєри (`|`) — передають вивід однієї команди на вхід іншої.  
  Напр.: `grep ... | wc -l` → кількість рядків, що відповідають шаблону.

- Цикли bash:  
  ```bash
  for f in 111 222 333; do grep -Hn "$f" "$f"; done
