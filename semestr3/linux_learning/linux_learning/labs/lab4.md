# ЛР №4 — Створення/копіювання/видалення/пошук та seq (усі варіанти)
# Підготовка (як у ЛР2)
#   - у робочому каталозі є city.txt
#   - працюємо з домашнього каталогу (`cd ~`)
#   - за потреби очищаємо артефакти попередніх запусків

# ========================= ВАРІАНТ 1 =========================
```bash
cd ~                                           # перехід у домашній каталог
rm -rf abc def; mkdir -p abc def               # почистити/створити каталоги abc і def

# B: імена файлів = перші слова рядків на 'B'; C: вміст = унікальні рядки
names=$(awk '/^B/{print $1}' city.txt | sort -u)   # витягти перші слова з рядків, що починаються на B, унікалізувати
content=$(sort -u city.txt)                         # вміст: усі унікальні рядки з city.txt

for d in abc def; do                                # для кожного каталогу abc і def...
  for n in $names; do printf '%s\n' "$content" > "$d/$n"; done
                                                   # ...створити файл з іменем $n і записати унікальний вміст
done

# D: файли з короткими іменами (<7) → E: перейменувати на <ім’я>.new
find abc def -type f -printf '%f\t%h\n' \          # вивести "basename<TAB>dirname" для кожного файла
 | awk 'length($1)<7 {print $2"/"$1}' \            # вибрати файли, де довжина basename < 7, зібрати повний шлях
 | xargs -I{} sh -c 'mv "{}" "{}".new'             # перейменувати: додаємо суфікс .new

# F1: /var/**/*.log → кількість рядків у кожному
sudo find /var -type f -name '*.log' -print0 \     # знайти всі .log (NUL-роздільник для безпечних імен)
 | xargs -0 -I{} sh -c 'wc -l "{}"'                # порахувати рядки у кожному лог-файлі
```

# ========================= ВАРІАНТ 2 =========================
```bash
cd ~                                           # у домашній каталог
rm -rf rrr; mkdir -p rrr                       # чистий майданчик rrr

# B: створити 1000 файлів 000..999; C: "Hello world"
seq -w 0 999 | xargs -I{} sh -c 'printf "Hello world\n" > rrr/{}'
                                                # для кожного номера створити файл із рядком "Hello world"

# D: імена починаються з 13 → E: перемістити у $HOME
find rrr -type f -name '13*' -exec mv -t "$HOME" {} +
                                                # усі файли, що починаються на "13", перенести у домашній каталог

# F2: /var/**/*.log → по 10 останніх рядків
sudo find /var -type f -name '*.log' -print0 \  # знайти усі .log
 | xargs -0 -I{} sh -c 'echo "===== {} ====="; tail -n 10 "{}"'
                                                # для кожного показати розділювач і останні 10 рядків
```

# ========================= ВАРІАНТ 3 =========================
```bash
cd ~                                           # дім
# A: q00..q99
for i in $(seq -w 0 99); do mkdir -p "q$i"; done   # створити каталоги q00..q99

# B: 1.txt у кожному; C: перші три рядки city.txt
head -n 3 city.txt > /tmp/first3.txt               # підготувати вміст
for i in $(seq -w 0 99); do cp /tmp/first3.txt "q$i/1.txt"; done
                                                   # скопіювати 1.txt у кожен q**

# D: імена закінчуються на 1 або 3 → E: зробити копію *.bak
find . -maxdepth 1 -type d -regex './q.*[13]$' \   # каталоги q.., що закінчуються 1 або 3
 | xargs -I{} sh -c 'cp "{}/1.txt" "{}/1.txt.bak" || true'
                                                   # зробити резервну копію, якщо 1.txt існує

# F3: ~/test a..f/A..Z
rm -rf ~/test; mkdir -p ~/test                     # новий корінь test
for a in a b c d e f; do for A in {A..Z}; do mkdir -p "$HOME/test/$a/$A"; done; done
                                                   # створити дерево a..f/A..Z
```

# ========================= ВАРІАНТ 4 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc/def abc/xyz abc/def/ghi/123 abc/def/ghi/456   # заготовка підкаталогів

# B: рядки, що починаються з "Be" (прибрати пробіли) → імена; C: "Hello world"
awk '/^Be/{gsub(/[[:space:]]+/,"",$0); print $0}' city.txt \  # взяти рядки на "Be" і прибрати пробіли
 | while read -r fname; do printf 'Hello world\n' > "abc/$fname"; done 2>/dev/null
                                                   # створити файли в abc з таким іменем і записати "Hello world"

# D: файли у abc та підкаталогах 1-го рівня → E: видалити
find abc -maxdepth 2 -type f -delete               # видалити всі файли на рівні ≤2

# F4: ~/test a..f/A..F/1..9
rm -rf ~/test; mkdir -p ~/test                     # чисто
for a in a b c d e f; do
  for A in A B C D E F; do
    for n in {1..9}; do mkdir -p "$HOME/test/$a/$A/$n"; done
  done
done                                               # дерево каталогів a..f/A..F/1..9
```

========================= ВАРІАНТ 5 =========================
```bash
cd ~
rm -rf ab c; mkdir -p ab c                         # два каталоги

# B: останні слова рядків → імена; C: перші 3 рядки city.txt
names=$(awk '{print $NF}' city.txt | sort -u)      # останнє поле кожного рядка, унікальне
head -n 3 city.txt > /tmp/first3.txt               # підготувати вміст
for d in ab c; do for n in $names; do cat /tmp/first3.txt > "$d/$n"; done; done
                                                   # створити файли з таким ім’ям у ab і c

# D: розмір від 5 до 22 байтів → E: вивести ім’я та розмір
find ab c -type f -size +4c -size -23c -printf '%p\t%s bytes\n'
                                                   # відфільтрувати за розміром і показати шлях + розмір

# F5: ~/test файли aa..zz
rm -rf ~/test; mkdir -p ~/test
for a in {a..z}; do for b in {a..z}; do : > "$HOME/test/$a$b"; done; done
                                                   # створити 26*26 порожніх файлів із дволітерними іменами
```

# ========================= ВАРІАНТ 6 =========================
```bash
cd ~
rm -rf qqq; mkdir -p qqq                           # робочий каталог

# B: другі слова рядків → імена; C: останні три рядки city.txt
names=$(awk 'NF>=2{print $2}' city.txt | sort -u)  # друге поле (якщо є)
tail -n 3 city.txt > /tmp/last3.txt                # підготувати вміст
for n in $names; do cat /tmp/last3.txt > "qqq/$n"; done
                                                   # створити файли з іменами з другого поля

# D: імена довші за 7 → E: вивести вміст
find qqq -type f -printf '%f\t%p\n' \              # basename<TAB>fullpath
 | awk 'length($1)>7 {print $2}' \                 # вибрати файли з довгим basename
 | xargs -I{} sh -c 'echo "===== {} ====="; cat "{}"'
                                                   # надрукувати маркер і вміст кожного

# F6: від / знайти файли, що починаються на .bash_
sudo find / -type f -name '.bash_*' 2>/dev/null    # ігнорувати помилки доступу
```

# ========================= ВАРІАНТ 7 =========================
```bash
cd ~
rm -rf qqq; mkdir -p qqq                           # робочий каталог

# B: другі слова рядків → імена; C: останні три рядки city.txt
names=$(awk 'NF>=2{print $2}' city.txt | sort -u)  # друге поле (якщо є)
tail -n 3 city.txt > /tmp/last3.txt                # підготувати вміст
for n in $names; do cat /tmp/last3.txt > "qqq/$n"; done
                                                   # створити файли з іменами з другого поля

# D: імена довші за 7 → E: вивести вміст
find qqq -type f -printf '%f\t%p\n' \              # basename<TAB>fullpath
 | awk 'length($1)>7 {print $2}' \                 # вибрати файли з довгим basename
 | xargs -I{} sh -c 'echo "===== {} ====="; cat "{}"'
                                                   # надрукувати маркер і вміст кожного

# F6: від / знайти файли, що починаються на .bash_
sudo find / -type f -name '.bash_*' 2>/dev/null    # ігнорувати помилки доступу
```

# ========================= ВАРІАНТ 8 =========================
```bash
cd ~
rm -rf ggg; mkdir -p ggg                           # чистий ggg

# B: створити файли з іменами з пробілами/без; C: "Hello world"
for n in "abc d" "ab c d" "abcd" "a b c d"; do printf 'Hello world\n' > "ggg/$n"; done
                                                   # демонстрація імен із пробілами (в лапках)

# D: в імені немає пробілів → E: вивести ім’я та зміст
find ggg -type f -printf '%f\t%p\n' | awk '$1 !~ / / {print $2}' \
 | xargs -I{} sh -c 'echo "===== {} ====="; cat "{}"'
                                                   # вибрати файли без пробілів у basename і показати їх

# F8: від / знайти файли, змінені від 5 до 3 днів тому
sudo find / -type f -mtime +3 -mtime -5 2>/dev/null # інтервал за модифікацією (3..5 днів тому)
```

# ========================= ВАРІАНТ 9 =========================
```bash
cd ~
# A: дерево 0/0/0 ... 9/9/9
for a in {0..9}; do for b in {0..9}; do for c in {0..9}; do mkdir -p "$a/$b/$c"; done; done; done
                                                   # трирівнева решітка каталогів 10×10×10

# B: у кожному каталозі створити 1.txt; C: "Hello world"
find . -regex './[0-9]/[0-9]/[0-9]$' -type d -exec sh -c 'printf "Hello world\n" > "$1/1.txt"' _ {} \;
                                                   # створити 1.txt у кожному листовому каталозі

# D: у повному імені файла є однакові цифри → E: вивести імена файлів
find . -type f -name '1.txt' -path './[0-9]/[0-9]/[0-9]/1.txt' \
 | grep -E '/([0-9]).*/\1/' \
 | sed 's#^\./##'
                                                   # вибрати ті шляхи, де перша і друга цифра шляху збігаються; надрукувати шлях без "./"

# F9: з $PATH → 10 найменших НЕпорожніх файлів → скопіювати в /root/test
sudo rm -rf /root/test; sudo mkdir -p /root/test
echo "$PATH" | tr ':' '\n' | while read d; do find "$d" -maxdepth 1 -type f -size +0c -printf '%s\t%p\n' 2>/dev/null; done \
 | sort -n | head -10 | cut -f2- \
 | while read f; do sudo cp -f "$f" /root/test/; done
                                                   # з кожного каталогу PATH зібрати файли з розмірами, взяти 10 найменших і скопіювати
```

# ========================= ВАРІАНТ 10 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc                           # чистий abc

# A: у abc відтворити структуру /usr/lib (каталоги)
sudo find /usr/lib -type d -printf '%P\n' | grep -v '^$' | xargs -I{} mkdir -p "abc/{}"
                                                   # віддзеркалити структуру каталогів

# B,C: не створювати файли

# D: каталоги рівня ≤ 2 відносно abc → E: у кожному створити порожній 1.txt
find abc -type d -mindepth 0 -maxdepth 2 -exec sh -c ': > "$1/1.txt"' _ {} \;
                                                   # у кожному каталозі до рівня 2 створити порожній файл

# F10: підкаталоги від /, де є файли, змінені за останні 24 год
sudo find / -type f -mtime -1 -printf '%h\n' 2>/dev/null | sort -u
                                                   # каталоги, що містять свіжі файли (унікалізовано)
```

# ========================= ВАРІАНТ 11 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc                           # чистий abc

# A: у abc відтворити структуру /usr/local (каталоги)
sudo find /usr/local -type d -printf '%P\n' | grep -v '^$' | xargs -I{} mkdir -p "abc/{}"
                                                   # віддзеркалити структуру /usr/local

# B,C: не створювати файли

# D: каталоги рівня ≥ 3 відносно abc → E: створити 1.txt з повним шляхом (від /)
find abc -type d -mindepth 3 \
 | while read -r d; do rel="${d#abc/}"; echo "/usr/local/$rel" > "$d/1.txt"; done
                                                   # записати у файл відновлений абсолютний шлях

# F11: /etc/passwd → bash-користувачі → скопіювати їх .bash_history у /root/test з іменем користувача
sudo rm -rf /root/test; sudo mkdir -p /root/test
sudo awk -F: '$7 ~ /\/bin\/bash$/ {print $1":"$6}' /etc/passwd \
 | while IFS=: read -r u home; do
     if sudo test -r "$home/.bash_history"; then
       sudo cp "$home/.bash_history" "/root/test/$u";
     fi
   done
                                                   # для кожного bash-користувача, якщо історія читається — копіюємо
```

# ========================= ВАРІАНТ 12 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc/def abc/xyz abc/def/ghi/123 abc/def/ghi/456   # дерево

# B: 1.txt у кожному каталозі з A; C: парні рядки з city.txt
awk 'NR%2==0' city.txt > /tmp/even.txt           # вибрати парні рядки
for d in abc abc/def abc/xyz abc/def/ghi/123 abc/def/ghi/456; do
  cat /tmp/even.txt > "$d/1.txt"                 # записати парні рядки у кожний 1.txt
done

# D: файли у підкаталогах рівня 2+ відносно abc → E: видалити
find abc -mindepth 2 -type d -exec find {} -maxdepth 1 -type f -name '1.txt' -delete \;
                                                   # видалити 1.txt починаючи з рівня 2

# F12: /etc (нерекурсивно) → файли у ~/files.txt, каталоги у ~/folders.txt
find /etc -mindepth 1 -maxdepth 1 -type f -printf '%f\n' > ~/files.txt
find /etc -mindepth 1 -maxdepth 1 -type d -printf '%f\n' > ~/folders.txt
                                                   # зберегти списки файлів і каталогів верхнього рівня /etc
```

# ========================= ВАРІАНТ 13 =========================
```bash
cd ~
rm -rf abc def hij; mkdir -p abc def hij          # три каталоги

# B: "Be..." (прибрати пробіли) → імена: створити порожні файли в abc/def/hij
awk '/^Be/{gsub(/[[:space:]]+/,"",$0); print $0}' city.txt \
 | while read -r fname; do : > "abc/$fname"; : > "def/$fname"; : > "hij/$fname"; done 2>/dev/null
                                                   # створити пусті файли з такими іменами у трьох каталогах

# D: довжина імені 20..50 → E: вивести ім’я та розмір
find abc def hij -type f -printf '%f\t%p\n' \     # basename<TAB>fullpath
 | awk 'length($1)>=20 && length($1)<=50 {print $2}' \  # фільтр за довжиною basename
 | xargs -I{} sh -c 'stat -c "%n %s bytes" "{}"'  # показати шлях і розмір у байтах (GNU stat)

# F13: знайти порожні файли у /home
sudo find /home -type f -empty 2>/dev/null        # усі zero-length файли (з ігнором помилок)
```

# ========================= ВАРІАНТ 14 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc/def abc/xyz abc/def/ghi/123 abc/def/ghi/456   # структура

# B: 1.txt; C: повний шлях + ім’я файлу (readlink -f дає абсолютний шлях)
for d in abc abc/def abc/xyz abc/def/ghi/123 abc/def/ghi/456; do
  f="$d/1.txt"; printf '%s\n' "$(readlink -f "$f")" > "$f"
done
                                                   # у кожний 1.txt записати його абсолютний шлях

# D: всі → E: вивести ім’я та вміст
find abc -type f -print | while read -r f; do echo "===== $f ====="; cat "$f"; done
                                                   # перелічити всі 1.txt і показати їхній вміст

# F14: у /usr знайти файли розміром > 10Мб
sudo find /usr -type f -size +10M 2>/dev/null     # великі файли, ігнорувати помилки доступу
```

# ========================= ВАРІАНТ 15 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc                           # чисто

# A: у abc відтворити структуру / до 3-го рівня вкладеності (каталоги)
sudo find / -mindepth 1 -maxdepth 3 -type d -printf '%P\n' 2>/dev/null \
 | grep -v '^$' | xargs -I{} mkdir -p "abc/{}"     # створити дзеркало перших 3 рівнів каталогів

# B,C: не створювати файли

# D: каталоги найбільшого рівня → E: створити файл з числом (рівень)
maxlvl=$(find abc -type d -printf '%d\n' | sort -nr | head -1)      # знайти максимальну глибину
find abc -type d -printf '%p\t%d\n' \                               # шлях і глибина
 | awk -v m="$maxlvl" '$2==m {print $1}' \                          # каталоги на максимальному рівні
 | xargs -I{} sh -c 'echo "$0" > "{}/level.txt"' "$maxlvl"          # записати число-рівень у level.txt

# F15: у /etc знайти *.conf → 10 з найбільшою кількістю рядків
sudo find /etc -type f -name '*.conf' -print0 \    # знайти конфіги (безпечно для імен)
 | xargs -0 -r wc -l 2>/dev/null | sort -nr | head -10
                                                   # порахувати рядки, відсортувати за спаданням, взяти топ-10
```

---

# Навігація та створення/видалення
- `cd ~` — перехід у домашній каталог.
- `mkdir -p PATH/...` — створює каталог(и); `-p` не ламається, якщо існують, та створює батьківські.
- `rm -rf NAME` — видаляє файли/каталоги рекурсивно (`-r`) без підтверджень (`-f`).
- `mv SRC DST` — перейменування/переміщення файлів/каталогів.
  - `mv -t DIR FILE...` — цільова директорія задається через `-t`.
- `cp SRC DST` — копіює файл.
  - `cp -f` — примусово (перезапис без запиту).

## Порожні файли та запис
- `: > file` — створює або **очищує** файл (перенаправлення порожнього stdout з no-op команди `:`).
- `printf 'TEXT\n' > file` — записує текст у файл (на відміну від `echo`, стабільно без зайвих символів).
- `echo TEXT` — друк тексту (спрощено; інколи замінений на `printf` для надійності).
- `cat file1 > file2` — копіює вміст (виводить file1 у stdout; тут перенаправляємо в file2).

## Генерація послідовностей та імен
- `seq -w 0 999` — числа `000…999` з вирівнюванням ширини (`-w`).
- Розширення діапазонів Bash:
  - `{A..Z}`, `{a..z}`, `{0..9}` — генерація літер/цифр у циклах.

## Пошук і добір файлів/каталогів — `find`
- Базові:
  - `find ROOT -type f|d` — шукає файли (`f`) або каталоги (`d`) від ROOT.
  - `-name '*.log'` — фільтр за шаблоном імені (globbing).
  - `-regex '...'` — фільтр за регулярним виразом шляху.
  - `-path '.../1.txt'` — фільтр за повним шляхом.
  - `-maxdepth N`, `-mindepth N` — обмеження глибини пошуку.
- Час/розмір:
  - `-mtime -5` — змінено **менше** ніж 5 днів тому.
  - `-mtime +3 -mtime -5` — змінено **між** 3 і 5 днів тому.
  - `-size +10M` — розмір більше 10 МіБ.
  - `-size +4c -size -23c` — розмір у байтах від 5 до 22.
- Вивід та дії:
  - `-print0` — нуль-роздільник для безпечної передачі в `xargs -0`.
  - `-printf 'FMT'` — форматований вивід (напр., `'%p\t%s\n'`, `'%f'` — лише ім’я, `'%h'` — директорія, `'%d'` — рівень глибини).
  - `-delete` — видалити знайдені файли.
  - `-exec CMD {} +` — виконати команду над групою знайдених об’єктів (ефективніше за `\;`).
- Приклади з ЛР:
  - `find abc -maxdepth 2 -type f -delete` — видалити файли в `abc` і підрівнях 1.
  - `sudo find /usr -type f -size +10M` — великі файли в `/usr`.

## Обробка потоків та списків — `xargs`, конвеєри, шели
- `xargs` — зчитує аргументи з stdin і формує виклики команди.
  - `xargs -0` — приймає нуль-терміновані записи (пара з `find -print0`).
  - `xargs -I {}` — шаблон підстановки (де вставляти аргумент).
  - `xargs -r` — не запускати команду, якщо ввід порожній.
- `sh -c 'SCRIPT' _ ARG` — виконати інлайн-скрипт оболонки; часто використовується з `xargs -I{}`.
- Конвеєри `|` — передають stdout однієї команди у stdin іншої.

## Текстова обробка
- `awk` — потужна пострічкова обробка тексту.
  - `awk 'умова{дія}' file`
  - Приклади:
    - `awk '/^B/{print $1}' city.txt` — перше слово у рядках, що починаються на `B`.
    - `awk '{print $NF}' city.txt` — останнє слово рядка.
    - `awk 'NR%2==0' city.txt` — парні рядки.
    - `gsub(/[[:space:]]+/,"",$0)` — прибрати всі пробіли з рядка.
    - Вивід рівня/поля: `print $1`, `print $2`, тощо.
- `sort` — сортування:
  - `sort -u` — відсортовані **унікальні** рядки.
  - `sort -n` — числове сортування.
  - `sort -r` — у зворотному порядку.
- `head -n 3 file` — перші 3 рядки.
- `tail -n 10 file` — останні 10 рядків.
- `grep` — пошук рядків за шаблоном/регекспом.
  - `grep -E '...|...'` — розширені регулярні вирази (альтернація `|` тощо).
- `tr ':' '\n'` — заміна символів (наприклад, розбити `$PATH` по `:` на рядки).
- `cut -f2-` — вирізати поля (тут — від другого до кінця, за табуляцією за замовчуванням).
- `sed 's#^\./##'` — прибрати префікс `./` зі шляхів.

## Перегляд/рахунок/метадані
- `wc -l file` — кількість рядків у файлі.
- `cat file` — показати вміст файлу.
- `stat -c "%n %s bytes" file` — ім’я та розмір у байтах.
- `readlink -f file` — повний (канонічний) шлях до файлу.

## Змінні оболонки та цикли
- Присвоєння: `names=$(command ...)`, використання: `for n in $names; do ...; done`
- Цикли:
  - `for a in ...; do ...; done`
  - Вкладені: `for a in {0..9}; do for b in ...; do ...; done; done`
  - Читання рядків: `while read -r x; do ...; done`
- Плейсхолдери в скриптах з `xargs -I{}`: `{}` буде підмінений поточним аргументом.