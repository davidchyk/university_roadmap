Зрозумів 👍
Ось усі 15 варіантів для ЛР №4 повністю у форматі .md (один блок коду, як у твоєму прикладі для ЛР №3):

# ЛР №4 — Створення/копіювання/видалення/пошук та seq (усі варіанти)
# Підготовка (як у ЛР2)
#   - у робочому каталозі є city.txt
#   - працюємо з домашнього каталогу (`cd ~`)
#   - за потреби очищаємо артефакти попередніх запусків

# ========================= ВАРІАНТ 1 =========================
```bash
cd ~
rm -rf abc def; mkdir -p abc def

# B: імена файлів = перші слова рядків, що починаються з 'B' у city.txt
# C: вміст = унікальні рядки з city.txt
names=$(awk '/^B/{print $1}' city.txt | sort -u)
content=$(sort -u city.txt)

for d in abc def; do
  for n in $names; do printf '%s\n' "$content" > "$d/$n"; done
done

# D: імена коротші за 7 символів → E: перейменувати на <ім’я>.new
find abc def -type f -printf '%f\t%h\n' \
 | awk 'length($1)<7 {print $2"/"$1}' \
 | xargs -I{} sh -c 'mv "{}" "{}".new'

# F1: /var/**/*.log → кількість рядків у кожному
sudo find /var -type f -name '*.log' -print0 \
 | xargs -0 -I{} sh -c 'wc -l "{}"'
```

# ========================= ВАРІАНТ 2 =========================
```bash
cd ~
rm -rf rrr; mkdir -p rrr

# B: створити 1000 файлів 000..999; C: "Hello world"
seq -w 0 999 | xargs -I{} sh -c 'printf "Hello world\n" > rrr/{}'

# D: імена починаються з 13 → E: перемістити у $HOME
find rrr -type f -name '13*' -exec mv -t "$HOME" {} +

# F2: /var/**/*.log → по 10 останніх рядків
sudo find /var -type f -name '*.log' -print0 \
 | xargs -0 -I{} sh -c 'echo "===== {} ====="; tail -n 10 "{}"'
```

# ========================= ВАРІАНТ 3 =========================
```bash
cd ~
# A: q00..q99
for i in $(seq -w 0 99); do mkdir -p "q$i"; done

# B: 1.txt у кожному; C: перші три рядки city.txt
head -n 3 city.txt > /tmp/first3.txt
for i in $(seq -w 0 99); do cp /tmp/first3.txt "q$i/1.txt"; done

# D: імена закінчуються на 1 або 3 → E: зробити копію *.bak
find . -maxdepth 1 -type d -regex './q.*[13]$' \
 | xargs -I{} sh -c 'cp "{}/1.txt" "{}/1.txt.bak" || true'

# F3: ~/test a..f/A..Z
rm -rf ~/test; mkdir -p ~/test
for a in a b c d e f; do for A in {A..Z}; do mkdir -p "$HOME/test/$a/$A"; done; done
```

# ========================= ВАРІАНТ 4 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc/def abc/xyz abc/def/ghi/123 abc/def/ghi/456

# B: рядки, що починаються з "Be" (пробіли видалити) → імена; C: "Hello world"
awk '/^Be/{gsub(/[[:space:]]+/,"",$0); print $0}' city.txt \
 | while read -r fname; do printf 'Hello world\n' > "abc/$fname"; done 2>/dev/null

# D: файли у abc та його підкаталогах 1-го рівня → E: видалити
find abc -maxdepth 2 -type f -delete

# F4: ~/test a..f/A..F/1..9
rm -rf ~/test; mkdir -p ~/test
for a in a b c d e f; do
  for A in A B C D E F; do
    for n in {1..9}; do mkdir -p "$HOME/test/$a/$A/$n"; done
  done
done
```

========================= ВАРІАНТ 5 =========================
```bash
cd ~
rm -rf ab c; mkdir -p ab c

# B: останні слова рядків city.txt → імена; C: перші 3 рядки city.txt
names=$(awk '{print $NF}' city.txt | sort -u)
head -n 3 city.txt > /tmp/first3.txt
for d in ab c; do for n in $names; do cat /tmp/first3.txt > "$d/$n"; done; done

# D: розмір від 5 до 22 байтів → E: вивести ім’я та розмір
find ab c -type f -size +4c -size -23c -printf '%p\t%s bytes\n'

# F5: ~/test файли aa..zz
rm -rf ~/test; mkdir -p ~/test
for a in {a..z}; do for b in {a..z}; do : > "$HOME/test/$a$b"; done; done
```

# ========================= ВАРІАНТ 6 =========================
```bash
cd ~
rm -rf qqq; mkdir -p qqq

# B: другі слова рядків → імена; C: останні три рядки city.txt
names=$(awk 'NF>=2{print $2}' city.txt | sort -u)
tail -n 3 city.txt > /tmp/last3.txt
for n in $names; do cat /tmp/last3.txt > "qqq/$n"; done

# D: імена довші за 7 → E: вивести вміст
find qqq -type f -printf '%f\t%p\n' \
 | awk 'length($1)>7 {print $2}' \
 | xargs -I{} sh -c 'echo "===== {} ====="; cat "{}"'

# F6: від / знайти файли, що починаються на .bash_
sudo find / -type f -name '.bash_*' 2>/dev/null
```

# ========================= ВАРІАНТ 7 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc

# A: у abc відтворити структуру підкаталогів /etc (каталоги)
sudo find /etc -type d -printf '%P\n' | grep -v '^$' | xargs -I{} mkdir -p "abc/{}"

# B: у кожному каталозі створити 1.txt; C: записати рівень (0 для abc)
find abc -type d -printf '%p\t%d\n' \
 | while read -r d depth; do echo "$depth" > "$d/1.txt"; done

# D: файли у каталогах рівня 2 відносно abc → E: вивести ім’я та зміст
find abc -mindepth 2 -maxdepth 2 -type f -print \
 | while read -r f; do echo "===== $f ====="; cat "$f"; done

# F7: від / знайти файли, змінені за останні 5 днів
sudo find / -type f -mtime -5 2>/dev/null
```

# ========================= ВАРІАНТ 8 =========================
```bash
cd ~
rm -rf ggg; mkdir -p ggg

# B: створити файли з іменами з пробілами/без; C: "Hello world"
for n in "abc d" "ab c d" "abcd" "a b c d"; do printf 'Hello world\n' > "ggg/$n"; done

# D: в імені немає пробілів → E: вивести ім’я та зміст
find ggg -type f -printf '%f\t%p\n' | awk '$1 !~ / / {print $2}' \
 | xargs -I{} sh -c 'echo "===== {} ====="; cat "{}"'

# F8: від / знайти файли, змінені від 5 до 3 днів тому
sudo find / -type f -mtime +3 -mtime -5 2>/dev/null
```

# ========================= ВАРІАНТ 9 =========================
```bash
cd ~
# A: дерево 0/0/0 ... 9/9/9
for a in {0..9}; do for b in {0..9}; do for c in {0..9}; do mkdir -p "$a/$b/$c"; done; done; done

# B: у кожному каталозі створити 1.txt; C: "Hello world"
find . -regex './[0-9]/[0-9]/[0-9]$' -type d -exec sh -c 'printf "Hello world\n" > "$1/1.txt"' _ {} \;

# D: у повному імені файлу є однакові цифри → E: вивести імена файлів
find . -type f -name '1.txt' -path './[0-9]/[0-9]/[0-9]/1.txt' \
 | grep -E '/([0-9]).*/\1/' \
 | sed 's#^\./##'

# F9: з $PATH → 10 найменших НЕпорожніх файлів → скопіювати в /root/test
sudo rm -rf /root/test; sudo mkdir -p /root/test
echo "$PATH" | tr ':' '\n' | while read d; do find "$d" -maxdepth 1 -type f -size +0c -printf '%s\t%p\n' 2>/dev/null; done \
 | sort -n | head -10 | cut -f2- \
 | while read f; do sudo cp -f "$f" /root/test/; done
```

# ========================= ВАРІАНТ 10 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc

# A: у abc відтворити структуру /usr/lib (каталоги)
sudo find /usr/lib -type d -printf '%P\n' | grep -v '^$' | xargs -I{} mkdir -p "abc/{}"

# B,C: не створювати файли

# D: каталоги рівня ≤ 2 відносно abc → E: у кожному створити порожній 1.txt
find abc -type d -mindepth 0 -maxdepth 2 -exec sh -c ': > "$1/1.txt"' _ {} \;

# F10: підкаталоги від /, де є файли, змінені за останні 24 год
sudo find / -type f -mtime -1 -printf '%h\n' 2>/dev/null | sort -u
```

# ========================= ВАРІАНТ 11 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc

# A: у abc відтворити структуру /usr/local (каталоги)
sudo find /usr/local -type d -printf '%P\n' | grep -v '^$' | xargs -I{} mkdir -p "abc/{}"

# B,C: не створювати файли

# D: каталоги рівня ≥ 3 відносно abc → E: створити 1.txt з повним шляхом (від /)
find abc -type d -mindepth 3 \
 | while read -r d; do rel="${d#abc/}"; echo "/usr/local/$rel" > "$d/1.txt"; done

# F11: /etc/passwd → bash-користувачі → скопіювати їх .bash_history у /root/test з іменем користувача
sudo rm -rf /root/test; sudo mkdir -p /root/test
sudo awk -F: '$7 ~ /\/bin\/bash$/ {print $1":"$6}' /etc/passwd \
 | while IFS=: read -r u home; do
     if sudo test -r "$home/.bash_history"; then
       sudo cp "$home/.bash_history" "/root/test/$u"; 
     fi
   done
```

# ========================= ВАРІАНТ 12 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc/def abc/xyz abc/def/ghi/123 abc/def/ghi/456

# B: 1.txt у кожному каталозі з A; C: парні рядки з city.txt
awk 'NR%2==0' city.txt > /tmp/even.txt
for d in abc abc/def abc/xyz abc/def/ghi/123 abc/def/ghi/456; do
  cat /tmp/even.txt > "$d/1.txt"
done

# D: файли у підкаталогах рівня 2 і далі відносно abc → E: видалити
find abc -mindepth 2 -type d -exec find {} -maxdepth 1 -type f -name '1.txt' -delete \;

# F12: /etc (нерекурсивно) → файли у ~/files.txt, каталоги у ~/folders.txt
find /etc -mindepth 1 -maxdepth 1 -type f -printf '%f\n' > ~/files.txt
find /etc -mindepth 1 -maxdepth 1 -type d -printf '%f\n' > ~/folders.txt
```

# ========================= ВАРІАНТ 13 =========================
```bash
cd ~
rm -rf abc def hij; mkdir -p abc def hij

# B: рядки, що починаються з "Be" (пробіли прибрати) → імена
awk '/^Be/{gsub(/[[:space:]]+/,"",$0); print $0}' city.txt \
 | while read -r fname; do : > "abc/$fname"; : > "def/$fname"; : > "hij/$fname"; done 2>/dev/null

# D: ДОВЖИНА ІМЕНІ від 20 до 50 символів → E: вивести ім’я та розмір
find abc def hij -type f -printf '%f\t%p\n' \
 | awk 'length($1)>=20 && length($1)<=50 {print $2}' \
 | xargs -I{} sh -c 'stat -c "%n %s bytes" "{}"'

# F13: знайти порожні файли у /home
sudo find /home -type f -empty 2>/dev/null
```

# ========================= ВАРІАНТ 14 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc/def abc/xyz abc/def/ghi/123 abc/def/ghi/456

# B: 1.txt; C: повний шлях + ім’я файлу
for d in abc abc/def abc/xyz abc/def/ghi/123 abc/def/ghi/456; do
  f="$d/1.txt"; printf '%s\n' "$(readlink -f "$f")" > "$f"
done

# D: всі → E: вивести ім’я та вміст
find abc -type f -print | while read -r f; do echo "===== $f ====="; cat "$f"; done

# F14: у /usr знайти файли розміром > 10Мб
sudo find /usr -type f -size +10M 2>/dev/null
```

# ========================= ВАРІАНТ 15 =========================
```bash
cd ~
rm -rf abc; mkdir -p abc

# A: у abc відтворити структуру / до 3-го рівня вкладеності (каталоги)
sudo find / -mindepth 1 -maxdepth 3 -type d -printf '%P\n' 2>/dev/null \
 | grep -v '^$' | xargs -I{} mkdir -p "abc/{}"

# B,C: не створювати файли

# D: каталоги найбільшого рівня → E: створити файл з числом (рівень)
maxlvl=$(find abc -type d -printf '%d\n' | sort -nr | head -1)
find abc -type d -printf '%p\t%d\n' \
 | awk -v m="$maxlvl" '$2==m {print $1}' \
 | xargs -I{} sh -c 'echo "$0" > "{}/level.txt"' "$maxlvl"

# F15: у /etc знайти *.conf → 10 з найбільшою кількістю рядків
sudo find /etc -type f -name '*.conf' -print0 \
 | xargs -0 -r wc -l 2>/dev/null | sort -nr | head -10
```