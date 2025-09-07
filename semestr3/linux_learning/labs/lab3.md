# ЛР №3 — Стандартні потоки, конвеєри, перенаправлення (усі варіанти)
# Підготовка (як у ЛР2)
#   - у робочому каталозі мають бути: test.txt, pass.txt (копія /etc/passwd), city.txt
#   - створюємо/очищуємо newfile.txt у кожному варіанті

# ========================= ВАРІАНТ 1 =========================
```bash
: > newfile.txt # опційно 
grep -E '\b[BRS][[:alpha:]]*[an]\b' city.txt | wc -l > newfile.txt
sort -r city.txt | grep -E '[68]$' >> newfile.txt
cat newfile.txt
ls > result.txt 2> error.txt
# F1 (root): bash-користувачі → їх $HOME (поле 6) → ls вмісту
sudo awk -F: '/\/bin\/bash/{print $6}' /etc/passwd | xargs -I {} ls {}
```

# ========================= ВАРІАНТ 2 =========================
```bash
: > newfile.txt # опційно
grep -E '\b[1][0-9]*[68]\b' city.txt | wc -l > newfile.txt
sort -u city.txt >> newfile.txt
cat newfile.txt
cdls > result.txt 2>&1
# F2 (user): /etc → *.conf та кількість рядків
cd /etc && ls *.conf | xargs wc -l
```

# ========================= ВАРІАНТ 3 =========================
```bash
: > newfile.txt # опційно
grep -i 'austria' city.txt | wc -l > newfile.txt
sort city.txt | uniq -d >> newfile.txt
cat newfile.txt
pwd > result.txt     # stderr — на екран (за замовч.)
# F3 (user): те саме, що F2
cd /etc && ls *.conf | xargs wc -l
```

# ========================= ВАРІАНТ 4 =========================
```bash
: > newfile.txt # опційно
grep -v 'Hungary' city.txt | wc -l > newfile.txt
sort city.txt | grep -E '^Be' >> newfile.txt
cat newfile.txt
pwpd 2> error.txt                         # stdout на екран, помилки у error.txt
# F4 (user): створити 111/222/333 і показати рядки, що містять ім’я файла; помилки у error.txt
cd ~
echo 111 > 111
echo 222 > yyy
echo 333 > 33343
for f in 111 222 333; do grep -Hn "$f" "$f"; done 2> error.txt
```

# ========================= ВАРІАНТ 5 =========================
```bash
: > newfile.txt # опційно
grep 'Spain' city.txt | wc -l > newfile.txt
sort city.txt | grep -E '^Be' >> newfile.txt
cat newfile.txt
lasts 2> error.txt                             # stdout на екран, помилки у error.txt
# F5 (user): у ~ у файлах [a-z]*.txt показати рядки з 'root'
cd ~ && grep -Hn 'root' [a-z]*.txt
```

# ========================= ВАРІАНТ 6 =========================
```bash
: > newfile.txt # опційно
grep -E '^[BM].*[678]$' city.txt | wc -l > newfile.txt
sort city.txt | grep -E '6$'>> newfile.txt
cat newfile.txt
ps > result.txt                                # stderr — на екран
# F6 (user): filelist.txt → вивести кожен файл, у потоці замінити A на ім’я файла; помилки у error.txt
cd ~
nano filelist.txt # filelist.txt має містити: pass.txt, city.txt, file123.txt
xargs -I {} sh -c 'sed "s/A/{}/g" "{}"' < filelist.txt 2> error.txt
```

# ========================= ВАРІАНТ 7 =========================
```bash
: > newfile.txt # опційно
grep -E '\b[[:alpha:]]{5}\b' city.txt | wc -l > newfile.txt
sort -r city.txt | grep -E '6$' >> newfile.txt
cat newfile.txt
sp > result.txt 2>&1                           # як у таблиці (команда навмисно некоректна)
# F7 (user): для кожного елемента з ls у /home — знайти збіг у /etc/passwd
for p in /home/*; do grep "$p" /etc/passwd; done
```

# ========================= ВАРІАНТ 8 =========================
```bash
: > newfile.txt # опційно
grep -Ev '\b[[:alpha:]]{5}\b' city.txt | wc -l > newfile.txt
sort city.txt | grep -E '^Ba' >> newfile.txt
cat newfile.txt
ls > result.txt                                 # stderr — на екран
# F8 (user): для кожного shell з /etc/shells (не коментар) знайти рядки у /etc/passwd
grep -v '^\s*#' /etc/shells | xargs -I {} grep {} /etc/passwd
```

# ========================= ВАРІАНТ 9 =========================
```bash
: > newfile.txt # опційно
grep -E '\b[[:alpha:]]{6}\b' city.txt | wc -l > newfile.txt
sort -u city.txt | grep -Ev 'Hungary|Spain' >> newfile.txt
cat newfile.txt
id > result.txt 2>&1
# F9 (root): bash-користувачі → імена → чи юзали sudo у /var/log/auth.log
sudo awk -F: '/\/bin\/bash/{print $1}' /etc/passwd | \
  while read u; do sudo grep -E "sudo.*$u" /var/log/auth.log; done
```

# ========================= ВАРІАНТ 10 =========================
```bash
: > newfile.txt # опційно
grep -Ev '\b[[:alpha:]]{6}\b' city.txt | wc -l > newfile.txt
sort city.txt | uniq -D >> newfile.txt
cat newfile.txt
ids > result.txt 2> error.txt
# F10 (user): унікальні рядки city.txt, що не починаються на B → створити <поле1>.text
awk '!/^B/{print $1}' city.txt | sort -u | xargs -I {} sh -c 'echo {} > {}.text'
```

# ========================= ВАРІАНТ 11 =========================
```bash
: > newfile.txt # опційно
grep -E '\b[[:alpha:]]{6}\b' city.txt | grep -Ev '\b[[:alpha:]]{8}\b' | wc -l > newfile.txt
sort city.txt | grep -E '^Be' >> newfile.txt
cat newfile.txt
lsmid 2> result.txt                            # stdout на екран
# F11 (user): PATH → каталоги → показати файли; помилки у error.txt
echo "$PATH" | tr ':' '\n' | xargs -I {} ls {} 2> error.txt
```

# ========================= ВАРІАНТ 12 =========================
```bash
: > newfile.txt # опційно
grep -E '\b[[:alpha:]]{6}\b' city.txt | grep -E '\b[[:alpha:]]{8}\b' | wc -l > newfile.txt
sort -u city.txt >> newfile.txt
cat newfile.txt
dirs > result.txt 2>&1
# F12 (root): /etc/passwd з /home/ і /bin/bash → імена → показати /home/<name>/.bash_history
sudo awk -F: '/\/home\// && /\/bin\/bash/{print $1}' /etc/passwd | \
  xargs -I {} sudo cat /home/{}/.bash_history
```

# ========================= ВАРІАНТ 13 =========================
```bash
: > newfile.txt # опційно
grep -Ev "Spain|Vienna" city.txt | wc -l > newfile.txt
sort city.txt | uniq -d >> newfile.txt
cat newfile.txt
ls 2> error.txt                                 # stdout на екран
# F13 (root): bash-користувачі → виконати id для кожного
sudo awk -F: '/\/bin\/bash/{print $1}' /etc/passwd | xargs -I {} sudo id {}
```

# ========================= ВАРІАНТ 14 =========================
```bash
: > newfile.txt # опційно
sort -u city.txt | grep -E '[357]$' | wc -l > newfile.txt
sort city.txt | uniq -D >> newfile.txt
cat newfile.txt
greb > result.txt 2>&1
# F14 (user): 2-ге поле city.txt → унікальні → відсортувати → взяти 3 → вивести <значення>.text; помилки у error.txt
awk '{print $2}' city.txt | sort -u | head -3 | xargs -I {} sh -c 'cat {}.text' 2> error.txt
```

# ========================= ВАРІАНТ 15 =========================
```bash
: > newfile.txt # опційно
grep -E '\b[[:alpha:]]*y\b' city.txt | wc -l > newfile.txt
sort -r city.txt | grep -E '8$'                 >> newfile.txt
cat newfile.txt
lsmod > result.txt                               # stderr — на екран
# F15 (user): файл зі списком користувачів → виконати id для кожного; помилки у error.txt
# (вихідний файл повинен містити рядки: user, root, test, nobody, daemon, man)
xargs -I {} id {} < users.txt 2> error.txt
```