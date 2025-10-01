# ЛР №6 — Управління користувачами, групами та правами доступу (усі варіанти)
# Підготовка (однакова для всіх варіантів)
#   - працювати під root (sudo -i) або перед командами додавати sudo
#   - використовуються утиліти: useradd, userdel, usermod, passwd, chown, chgrp, chmod

---

# ========================= ВАРІАНТ 1 =========================
```bash
useradd -m -d /home/lucia lucia          # створити користувача lucia з домашнім /home/lucia
useradd -m -d /home/maria maria          # створити користувача maria
useradd -m -d /home/sofia sofia          # створити користувача sofia

passwd lucia                              # встановити пароль lucia
passwd maria                              # встановити пароль maria
passwd sofia                              # встановити пароль sofia

usermod -c "Rodriguez" lucia              # GECOS-коментар (прізвище) для lucia
usermod -c "Fernandez" maria              # коментар для maria
usermod -c "Gonzalez" sofia               # коментар для sofia

usermod -d /home/gonzalez -m sofia        # перенести домашній каталог sofia → /home/gonzalez (із копіюванням)

groupadd spain                            # створити групу spain
usermod -aG spain lucia                   # додати lucia у групу spain
usermod -aG spain maria                   # додати maria у групу spain
usermod -aG spain sofia                   # додати sofia у групу spain

mkdir /home/spain                         # створити каталог /home/spain
chown lucia:spain /home/spain             # власник lucia, група spain

su - lucia -c 'echo hello > /home/spain/test.txt'  # створити файл test.txt від імені lucia
chmod 600 /home/spain/test.txt            # права: rw------- (лише власник)
chmod 620 /home/spain/test.txt            # права: rw- (owner), -w- (group), --- (others)
```
# ========================= ВАРІАНТ 2 =========================
```bash

useradd -m -d /home/hugo hugo             # створити користувача hugo з домівкою /home/hugo
useradd -m -d /home/daniel daniel         # створити користувача daniel
useradd -m -d /home/pablo pablo           # створити користувача pablo
passwd hugo; passwd daniel; passwd pablo  # встановити паролі трьом користувачам

usermod -c "Garcia" hugo                  # коментар (прізвище) для hugo
usermod -c "Lopez" daniel                 # коментар для daniel
usermod -c "Martinez" pablo               # коментар для pablo

usermod -d /home/martinez -m pablo        # перенести домівку pablo → /home/martinez

groupadd spain                            # створити групу spain
usermod -aG spain hugo                    # додати hugo у spain
usermod -aG spain daniel                  # додати daniel у spain
usermod -aG spain pablo                   # додати pablo у spain
mkdir /home/spain                         # створити каталог групи
chown hugo:spain /home/spain              # власник hugo, група spain

su - hugo -c 'echo hi > /home/spain/test.txt'  # створити test.txt від імені hugo
chmod 600 /home/spain/test.txt            # rw------- (лише власник)
chmod 620 /home/spain/test.txt            # rw- для власника, -w- для групи

```
# ========================= ВАРІАНТ 3 =========================
```bash

useradd -m gabriel                        # створити користувача gabriel (домівка /home/gabriel)
useradd -m adam                           # створити користувача adam
useradd -m raphael                        # створити користувача raphael
passwd gabriel; passwd adam; passwd raphael   # встановити паролі трьом

usermod -c "Martin" gabriel               # коментар (прізвище) для gabriel
usermod -c "Bernard" adam                 # коментар для adam
usermod -c "Dubois" raphael               # коментар для raphael

usermod -d /home/dubois -m raphael        # перенести домівку raphael → /home/dubois

groupadd france                           # створити групу france
usermod -aG france gabriel                # додати gabriel у france
usermod -aG france adam                   # додати adam у france
usermod -aG france raphael                # додати raphael у france
mkdir /home/france                        # створити /home/france
chown gabriel:france /home/france         # власник gabriel, група france


```
# ========================= ВАРІАНТ 4 =========================
```bash

useradd -m louise                         # створити louise
useradd -m alice                          # створити alice
useradd -m chloe                          # створити chloe
passwd louise; passwd alice; passwd chloe # паролі

usermod -c "Durand" louise                # коментар для louise
usermod -c "Leroy" alice                  # коментар для alice
usermod -c "Moreau" chloe                 # коментар для chloe

usermod -d /home/moreau -m chloe          # перенести домівку chloe → /home/moreau

groupadd france                           # створити групу france
usermod -aG france louise                 # додати louise
usermod -aG france alice                  # додати alice
usermod -aG france chloe                  # додати chloe
mkdir /home/france                        # створити каталог групи
chown louise:france /home/france          # власник louise, група france

```
# ========================= ВАРІАНТ 5 =========================
```bash

useradd -m lukas                          # створити lukas
useradd -m maximilian                     # створити maximilian
useradd -m jakob                          # створити jakob
passwd lukas; passwd maximilian; passwd jakob  # паролі

usermod -c "Gruber" lukas                 # коментар для lukas
usermod -c "Huber" maximilian             # коментар для maximilian
usermod -c "Bauer" jakob                  # коментар для jakob

usermod -d /home/bauer -m jakob           # перенести домівку jakob → /home/bauer

groupadd austria                          # створити групу austria
usermod -aG austria lukas                 # додати lukas
usermod -aG austria maximilian            # додати maximilian
usermod -aG austria jakob                 # додати jakob
mkdir /home/austria                       # створити /home/austria
chown lukas:austria /home/austria         # власник lukas, група austria

```
# ========================= ВАРІАНТ 6 =========================
```bash

useradd -m ana                            # створити ana
useradd -m sophia                         # створити sophia
useradd -m emma                           # створити emma
passwd ana; passwd sophia; passwd emma    # паролі

usermod -c "Wagner" ana                   # коментар для ana
usermod -c "Muller" sophia                # коментар для sophia
usermod -c "Pichler" emma                 # коментар для emma

usermod -d /home/pichler -m emma          # перенести домівку emma → /home/pichler

groupadd austria                          # група austria
usermod -aG austria ana                   # додати ana
usermod -aG austria sophia                # додати sophia
usermod -aG austria emma                  # додати emma
mkdir /home/austria                       # створити /home/austria
chown ana:austria /home/austria           # власник ana, група austria
```
# ========================= ВАРІАНТ 7 =========================
```bash

useradd -m sofia                          # створити sofia
useradd -m giulia                         # створити giulia
useradd -m aurora                         # створити aurora
passwd sofia; passwd giulia; passwd aurora  # паролі

usermod -c "Rossi" sofia                  # коментар для sofia
usermod -c "Ricci" giulia                 # коментар для giulia
usermod -c "Conti" aurora                 # коментар для aurora

usermod -d /home/conti -m aurora          # перенести домівку aurora → /home/conti

groupadd italy                            # створити групу italy
usermod -aG italy sofia                   # додати sofia
usermod -aG italy giulia                  # додати giulia
usermod -aG italy aurora                  # додати aurora
mkdir /home/italy                         # створити /home/italy
chown sofia:italy /home/italy             # власник sofia, група italy

```
# ========================= ВАРІАНТ 8 =========================
```bash

useradd -m francesco                      # створити francesco
useradd -m alessandro                     # створити alessandro
useradd -m lorenzo                        # створити lorenzo
passwd francesco; passwd alessandro; passwd lorenzo  # паролі

usermod -c "Marino" francesco             # коментар для francesco
usermod -c "Lombardi" alessandro          # коментар для alessandro
usermod -c "Barbieri" lorenzo             # коментар для lorenzo

usermod -d /home/barbieri -m lorenzo      # перенести домівку lorenzo → /home/barbieri

groupadd italy                            # група italy
usermod -aG italy francesco               # додати francesco
usermod -aG italy alessandro              # додати alessandro
usermod -aG italy lorenzo                 # додати lorenzo
mkdir /home/italy                         # створити /home/italy
chown francesco:italy /home/italy         # власник francesco, група italy

```
# ========================= ВАРІАНТ 9 =========================
``` bash
useradd -m jakub                          # створити jakub
useradd -m jan                            # створити jan
useradd -m tomas                          # створити tomas
passwd jakub; passwd jan; passwd tomas    # паролі

usermod -c "Novak" jakub                  # коментар для jakub
usermod -c "Svoboda" jan                  # коментар для jan
usermod -c "Novotny" tomas                # коментар для tomas

usermod -d /home/novotny -m tomas         # перенести домівку tomas → /home/novotny

groupadd czech                            # створити групу czech
usermod -aG czech jakub                   # додати jakub
usermod -aG czech jan                     # додати jan
usermod -aG czech tomas                   # додати tomas
mkdir /home/czech                         # створити /home/czech
chown jakub:czech /home/czech             # власник jakub, група czech

```
# ========================= ВАРІАНТ 10 =========================
```bash

useradd -m eliska                         # створити eliska
useradd -m tereza                         # створити tereza
useradd -m anna                           # створити anna
passwd eliska; passwd tereza; passwd anna # паролі

usermod -c "Dvorakova" eliska             # коментар для eliska
usermod -c "Cerna" tereza                 # коментар для tereza
usermod -c "Vesela" anna                  # коментар для anna

usermod -d /home/vesela -m anna           # перенести домівку anna → /home/vesela

groupadd czech                            # група czech
usermod -aG czech eliska                  # додати eliska
usermod -aG czech tereza                  # додати tereza
usermod -aG czech anna                    # додати anna
mkdir /home/czech                         # створити /home/czech
chown eliska:czech /home/czech            # власник eliska, група czech

```
# ========================= ВАРІАНТ 11 =========================
```bash

useradd -m emma                           # створити emma
useradd -m nora                           # створити nora
useradd -m sara                           # створити sara
passwd emma; passwd nora; passwd sara     # паролі

usermod -c "Hansen" emma                  # коментар для emma
usermod -c "Olsen" nora                   # коментар для nora
usermod -c "Johansen" sara                # коментар для sara

usermod -d /home/johansen -m sara         # перенести домівку sara → /home/johansen

groupadd norway                           # група norway
usermod -aG norway emma                   # додати emma
usermod -aG norway nora                   # додати nora
usermod -aG norway sara                   # додати sara
mkdir /home/norway                        # створити /home/norway
chown emma:norway /home/norway            # власник emma, група norway

```
# ========================= ВАРІАНТ 12 =========================
```bash

useradd -m william                        # створити william
useradd -m mathias                        # створити mathias
useradd -m oliver                         # створити oliver
passwd william; passwd mathias; passwd oliver  # паролі

usermod -c "Larsen" william               # коментар для william
usermod -c "Andersen" mathias             # коментар для mathias
usermod -c "Nilsen" oliver                # коментар для oliver

usermod -d /home/nilsen -m oliver         # перенести домівку oliver → /home/nilsen

groupadd norway                           # група norway
usermod -aG norway william                # додати william
usermod -aG norway mathias                # додати mathias
usermod -aG norway oliver                 # додати oliver
mkdir /home/norway                        # створити /home/norway
chown william:norway /home/norway         # власник william, група norway
```
# ========================= ВАРІАНТ 13 =========================
```bash
useradd -m andrei                         # створити andrei
useradd -m alexandru                      # створити alexandru
useradd -m stefan                         # створити stefan
passwd andrei; passwd alexandru; passwd stefan  # паролі

usermod -c "Radu" andrei                  # коментар для andrei
usermod -c "Stan" alexandru               # коментар для alexandru
usermod -c "Popescu" stefan               # коментар для stefan

usermod -d /home/popescu -m stefan        # перенести домівку stefan → /home/popescu

groupadd romania                          # група romania
usermod -aG romania andrei                # додати andrei
usermod -aG romania alexandru             # додати alexandru
usermod -aG romania stefan                # додати stefan
mkdir /home/romania                       # створити /home/romania
chown andrei:romania /home/romania        # власник andrei, група romania
```
# ========================= ВАРІАНТ 14 =========================
```bash

useradd -m anamaria                       # створити anamaria (без дефіса у login)
useradd -m maria                          # створити maria
useradd -m elena                          # створити elena
passwd anamaria; passwd maria; passwd elena  # паролі

usermod -c "Ciobanu" anamaria             # коментар для anamaria
usermod -c "Ionescu" maria                # коментар для maria
usermod -c "Dimitru" elena                # коментар для elena

usermod -d /home/dimitru -m elena         # перенести домівку elena → /home/dimitru

groupadd romania                          # група romania
usermod -aG romania anamaria              # додати anamaria
usermod -aG romania maria                 # додати maria
usermod -aG romania elena                 # додати elena
mkdir /home/romania                       # створити /home/romania
chown anamaria:romania /home/romania      # власник anamaria, група romania

```
# ========================= ВАРІАНТ 15 =========================
```bash
useradd -m nikola                         # створити nikola
useradd -m luca                           # створити luca
useradd -m stefan                         # створити stefan
passwd nikola; passwd luca; passwd stefan # паролі

usermod -c "Jovanovic" nikola             # коментар для nikola
usermod -c "Petrovic" luca                # коментар для luca
usermod -c "Nikolic" stefan               # коментар для stefan

usermod -d /home/nikolic -m stefan        # перенести домівку stefan → /home/nikolic

groupadd serbia                           # група serbia
usermod -aG serbia nikola                 # додати nikola
usermod -aG serbia luca                   # додати luca
usermod -aG serbia stefan                 # додати stefan
mkdir /home/serbia                        # створити /home/serbia
chown nikola:serbia /home/serbia          # власник nikola, група serbia

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