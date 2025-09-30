# ЛР №6 — Управління користувачами, групами та правами доступу (усі варіанти)
# Підготовка (однакова для всіх варіантів)
#   - працювати під root (sudo -i) або перед командами додавати sudo
#   - використовуються утиліти: useradd, userdel, usermod, passwd, chown, chgrp, chmod

---

# ========================= ВАРІАНТ 1 =========================
```bash
# A: Lucia, Maria, Sofia
useradd -m -d /home/lucia lucia
useradd -m -d /home/maria maria
useradd -m -d /home/sofia sofia

passwd lucia
passwd maria
passwd sofia

# B: прізвища Rodriguez, Fernandez, Gonzalez
usermod -c "Rodriguez" lucia
usermod -c "Fernandez" maria
usermod -c "Gonzalez" sofia

# Перенесення домашнього каталогу 3-го користувача
usermod -d /home/gonzalez -m sofia

# C: група spain
groupadd spain
usermod -aG spain lucia
usermod -aG spain maria
usermod -aG spain sofia

# Каталог /home/spain
mkdir /home/spain
chown lucia:spain /home/spain

# test.txt з правами тільки для lucia (читати) і root
su - lucia -c 'echo hello > /home/spain/test.txt'
chmod 600 /home/spain/test.txt
ls -l /home/spain/test.txt

# Дати групі spain право писати, lucia (власник) право читати
chmod 620 /home/spain/test.txt
```
# ========================= ВАРІАНТ 2 =========================
```bash

# A: Hugo, Daniel, Pablo
useradd -m -d /home/hugo hugo
useradd -m -d /home/daniel daniel
useradd -m -d /home/pablo pablo
passwd hugo; passwd daniel; passwd pablo

# B: Garcia, Lopez, Martinez
usermod -c "Garcia" hugo
usermod -c "Lopez" daniel
usermod -c "Martinez" pablo

# move home of 3rd user
usermod -d /home/martinez -m pablo

# C: group spain
groupadd spain
usermod -aG spain hugo daniel pablo
mkdir /home/spain
chown hugo:spain /home/spain

# test.txt права
su - hugo -c 'echo hi > /home/spain/test.txt'
chmod 600 /home/spain/test.txt
chmod 620 /home/spain/test.txt
```
# ========================= ВАРІАНТ 3 =========================
```bash

# A: Gabriel, Adam, Raphael
useradd -m gabriel; useradd -m adam; useradd -m raphael
passwd gabriel; passwd adam; passwd raphael

# B: Martin, Bernard, Dubois
usermod -c "Martin" gabriel
usermod -c "Bernard" adam
usermod -c "Dubois" raphael

usermod -d /home/dubois -m raphael

# C: france
groupadd france
usermod -aG france gabriel adam raphael
mkdir /home/france
chown gabriel:france /home/france
```
# ========================= ВАРІАНТ 4 =========================
```bash

# A: Louise, Alice, Chloe
useradd -m louise; useradd -m alice; useradd -m chloe
passwd louise; passwd alice; passwd chloe

# B: Durand, Leroy, Moreau
usermod -c "Durand" louise
usermod -c "Leroy" alice
usermod -c "Moreau" chloe

usermod -d /home/moreau -m chloe

# C: france
groupadd france
usermod -aG france louise alice chloe
mkdir /home/france
chown louise:france /home/france
```
# ========================= ВАРІАНТ 5 =========================
```bash

# A: Lukas, Maximilian, Jakob
useradd -m lukas; useradd -m maximilian; useradd -m jakob
passwd lukas; passwd maximilian; passwd jakob

# B: Gruber, Huber, Bauer
usermod -c "Gruber" lukas
usermod -c "Huber" maximilian
usermod -c "Bauer" jakob

usermod -d /home/bauer -m jakob

# C: austria
groupadd austria
usermod -aG austria lukas maximilian jakob
mkdir /home/austria
chown lukas:austria /home/austria
```
# ========================= ВАРІАНТ 6 =========================
```bash

# A: Ana, Sophia, Emma
useradd -m ana; useradd -m sophia; useradd -m emma
passwd ana; passwd sophia; passwd emma

# B: Wagner, Muller, Pichler
usermod -c "Wagner" ana
usermod -c "Muller" sophia
usermod -c "Pichler" emma

usermod -d /home/pichler -m emma

# C: austria
groupadd austria
usermod -aG austria ana sophia emma
mkdir /home/austria
chown ana:austria /home/austria
```
# ========================= ВАРІАНТ 7 =========================
```bash

# A: Sofia, Giulia, Aurora
useradd -m sofia; useradd -m giulia; useradd -m aurora
passwd sofia; passwd giulia; passwd aurora

# B: Rossi, Ricci, Conti
usermod -c "Rossi" sofia
usermod -c "Ricci" giulia
usermod -c "Conti" aurora

usermod -d /home/conti -m aurora

# C: italy
groupadd italy
usermod -aG italy sofia giulia aurora
mkdir /home/italy
chown sofia:italy /home/italy
```
# ========================= ВАРІАНТ 8 =========================
```bash

# A: Francesco, Alessandro, Lorenzo
useradd -m francesco; useradd -m alessandro; useradd -m lorenzo
passwd francesco; passwd alessandro; passwd lorenzo

# B: Marino, Lombardi, Barbieri
usermod -c "Marino" francesco
usermod -c "Lombardi" alessandro
usermod -c "Barbieri" lorenzo

usermod -d /home/barbieri -m lorenzo

# C: italy
groupadd italy
usermod -aG italy francesco alessandro lorenzo
mkdir /home/italy
chown francesco:italy /home/italy
```
# ========================= ВАРІАНТ 9 =========================
``` bash
# A: Jakub, Jan, Tomas
useradd -m jakub; useradd -m jan; useradd -m tomas
passwd jakub; passwd jan; passwd tomas

# B: Novak, Svoboda, Novotny
usermod -c "Novak" jakub
usermod -c "Svoboda" jan
usermod -c "Novotny" tomas

usermod -d /home/novotny -m tomas

# C: czech
groupadd czech
usermod -aG czech jakub jan tomas
mkdir /home/czech
chown jakub:czech /home/czech
```
# ========================= ВАРІАНТ 10 =========================
```bash

# A: Eliska, Tereza, Anna
useradd -m eliska; useradd -m tereza; useradd -m anna
passwd eliska; passwd tereza; passwd anna

# B: Dvorakova, Cerna, Vesela
usermod -c "Dvorakova" eliska
usermod -c "Cerna" tereza
usermod -c "Vesela" anna

usermod -d /home/vesela -m anna

# C: czech
groupadd czech
usermod -aG czech eliska tereza anna
mkdir /home/czech
chown eliska:czech /home/czech
```
# ========================= ВАРІАНТ 11 =========================
```bash

# A: Emma, Nora, Sara
useradd -m emma; useradd -m nora; useradd -m sara
passwd emma; passwd nora; passwd sara

# B: Hansen, Olsen, Johansen
usermod -c "Hansen" emma
usermod -c "Olsen" nora
usermod -c "Johansen" sara

usermod -d /home/johansen -m sara

# C: norway
groupadd norway
usermod -aG norway emma nora sara
mkdir /home/norway
chown emma:norway /home/norway
```
# ========================= ВАРІАНТ 12 =========================
```bash

# A: William, Mathias, Oliver
useradd -m william; useradd -m mathias; useradd -m oliver
passwd william; passwd mathias; passwd oliver

# B: Larsen, Andersen, Nilsen
usermod -c "Larsen" william
usermod -c "Andersen" mathias
usermod -c "Nilsen" oliver

usermod -d /home/nilsen -m oliver

# C: norway
groupadd norway
usermod -aG norway william mathias oliver
mkdir /home/norway
chown william:norway /home/norway
```
# ========================= ВАРІАНТ 13 =========================
```bash

# A: Andrei, Alexandru, Stefan
useradd -m andrei; useradd -m alexandru; useradd -m stefan
passwd andrei; passwd alexandru; passwd stefan

# B: Radu, Stan, Popescu
usermod -c "Radu" andrei
usermod -c "Stan" alexandru
usermod -c "Popescu" stefan

usermod -d /home/popescu -m stefan

# C: romania
groupadd romania
usermod -aG romania andrei alexandru stefan
mkdir /home/romania
chown andrei:romania /home/romania
```
# ========================= ВАРІАНТ 14 =========================
```bash

# A: Ana-Maria, Maria, Elena
useradd -m anamaria; useradd -m maria; useradd -m elena
passwd anamaria; passwd maria; passwd elena

# B: Ciobanu, Ionescu, Dimitru
usermod -c "Ciobanu" anamaria
usermod -c "Ionescu" maria
usermod -c "Dimitru" elena

usermod -d /home/dimitru -m elena

# C: romania
groupadd romania
usermod -aG romania anamaria maria elena
mkdir /home/romania
chown anamaria:romania /home/romania
```
# ========================= ВАРІАНТ 15 =========================
```bash

# A: Nikola, Luca, Stefan
useradd -m nikola; useradd -m luca; useradd -m stefan
passwd nikola; passwd luca; passwd stefan

# B: Jovanovic, Petrovic, Nikolic
usermod -c "Jovanovic" nikola
usermod -c "Petrovic" luca
usermod -c "Nikolic" stefan

usermod -d /home/nikolic -m stefan

# C: serbia
groupadd serbia
usermod -aG serbia nikola luca stefan
mkdir /home/serbia
chown nikola:serbia /home/serbia
```

---

# Перелік команд і опцій, що використовуються в ЛР №6 (і що вони роблять)

## Керування користувачами
- `useradd NAME` — створює **обліковий запис** (тільки записи в /etc/passwd|/etc/shadow).
  - `-m` — створити **домашній каталог** (`/home/NAME`) і скопіювати скелет (`/etc/skel`).
  - `-d /home/XYZ` — вказати **інший шлях** до домашнього каталогу.
- `passwd NAME` — встановити/змінити **пароль** користувача (оновлює `/etc/shadow`).
- `usermod` — змінює параметри існуючого користувача:
  - `-c "COMMENT"` — встановити **GECOS-коментар** (часто прізвище, ПІБ).
  - `-d /new/home -m` — **перенести** домашній каталог у нове місце (з копіюванням вмісту).
  - `-aG GROUP1[,GROUP2...]` — **додати** у додаткові групи (**а**ppend до існуючих).
    - Без `-a` перезаписує список додаткових груп!
- `userdel NAME` — видалити користувача.
  - `-r` — видалити **домашній каталог** та пошту користувача.

## Керування групами
- `groupadd NAME` — створити нову **групу**.
- `gpasswd -a USER GROUP` / `gpasswd -d USER GROUP` — додати/прибрати користувача з групи (альтернатива `usermod -aG`).

## Власник/група/права (ACL класика)
- `chown USER:GROUP PATH` — змінити **власника** та/або **групу** файла/каталогу.
  - приклад: `chown lucia:spain /home/spain`
- `chgrp GROUP PATH` — змінити **групу** (коли власник лишається тим самим).
- `chmod MODE PATH` — змінити **права доступу**.
  - **цифрові режими**: `UGO` як **власник/група/інші** (бінарні біти `r=4, w=2, x=1`):
    - `600` → `rw-------` (читати/писати лише власник).
    - `620` → `rw- -w- ---` (власник `rw`, група `w`, іншим — нічого) — приклад із `test.txt`.
  - **символьні режими**: `u/g/o/a +/- r|w|x` (не використовувалося в ЛР, але корисно).
- `ls -l PATH` — показати права/власника/групу: наприклад, перевірка `test.txt`.

## Перехід користувачем та виконання команд
- `su - USER -c 'CMD'` — виконати **команду від імені USER** з логін-шелом (`-` читає профілі).
  - приклад: створення файлу в каталозі, що належить користувачу:  
    `su - lucia -c 'echo hello > /home/spain/test.txt'`

## Допоміжні файлові операції (для сценаріїв ЛР)
- `mkdir /home/spain` — створити каталог призначення.
- `echo TEXT > file` — записати текст у файл (створити/перезаписати).