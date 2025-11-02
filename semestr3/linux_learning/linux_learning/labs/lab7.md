# ЛР №7 — Пакетні менеджери, динамічні бібліотеки, створення пакета (усі варіанти)
> Середовище: Debian/Ubuntu/Mint (apt + dpkg). У кожному варіанті дублюється підготовка.

# ========================= ВАРІАНТ 1 =========================
```bash
# Підготовка
sudo apt update                         # оновити список доступних пакетів
apt list --installed                    # показати перелік встановлених пакетів
sudo apt install -y mc                  # встановити mc (Midnight Commander), підтвердити автоматично
mc --version                            # перевірити версію mc
ldd "$(command -v mc)"                  # вивести список бібліотек, від яких залежить виконуваний файл mc

# A1: Вивести 'Hello world'
cat > lab7 <<'SH'                       # створити файл lab7 зі вмістом нижче (через here-doc)
#!/usr/bin/env bash
echo "Hello world"                      # скрипт просто виведе Hello world
SH
chmod +x lab7                           # зробити скрипт виконуваним

# Пакування
PKN=lab7-v01; VER=1.0                   # встановити змінні: ім’я пакета та версія
rm -rf "$HOME/build/$PKN"               # очистити попередню збірку
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # створити структуру директорій
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # скопіювати скрипт з правами 0755
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF    # створити метадані пакету (файл control)
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"   # зібрати .deb пакет
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                              # встановити пакет
lab7 || true                         # виконати встановлений скрипт (ігнорувати помилки)
sudo dpkg -r $PKN                     # видалити пакет

```
# ========================= ВАРІАНТ 2 =========================
```bash

# Підготовка
sudo apt update                         # оновити список доступних пакетів
apt list --installed                    # показати перелік встановлених пакетів
sudo apt install -y mc                  # встановити mc
mc --version                            # перевірити версію mc
ldd "$(command -v mc)"                  # показати бібліотеки, від яких залежить mc

# A2: приймає рядок, виводить кількість символів
cat > lab7 <<'SH'                       # створити скрипт lab7
#!/usr/bin/env bash
s="${1-}"                               # взяти перший аргумент, якщо є
echo "${#s}"                            # вивести кількість символів у рядку
SH
chmod +x lab7                           # зробити скрипт виконуваним

# Пакування
PKN=lab7-v02; VER=1.0                   # ім’я пакету та версія
rm -rf "$HOME/build/$PKN"               # видалити попередню збірку
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # створити структуру
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # скопіювати скрипт у bin
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF    # створити метадані пакету
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"   # зібрати .deb
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                              # встановити пакет
lab7 "mint" || true                 # викликати скрипт із параметром "mint"
sudo dpkg -r $PKN                     # видалити пакет

```
# ========================= ВАРІАНТ 3 =========================
```bash

# Підготовка
sudo apt update                         # оновити список пакетів
apt list --installed                    # вивести список встановлених
sudo apt install -y mc                  # встановити mc
mc --version                            # перевірити версію
ldd "$(command -v mc)"                  # перевірити залежності бібліотек

# A3: приймає n, виводить 1..n
cat > lab7 <<'SH'                       # створити скрипт
#!/usr/bin/env bash
n="${1?Usage: lab7 <n>}"                # аргумент n, якщо відсутній → помилка
seq 1 "$n" | paste -sd' ' -             # надрукувати числа від 1 до n через пробіл
SH
chmod +x lab7                           # зробити скрипт виконуваним

# Пакування
PKN=lab7-v03; VER=1.0                   # ім’я та версія пакету
rm -rf "$HOME/build/$PKN"               # видалити стару збірку
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # каталоги
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # встановити скрипт
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF    # метадані
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"   # зібрати пакет
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                              # інсталювати
lab7 5 || true                      # викликати скрипт із параметром 5
sudo dpkg -r $PKN                     # видалити пакет

```
# ========================= ВАРІАНТ 4 =========================
```bash

# Підготовка
sudo apt update                         # апдейт індексів
apt list --installed                    # список пакунків
sudo apt install -y mc                  # інсталяція mc
mc --version                            # версія
ldd "$(command -v mc)"                  # залежності

# A4: Приймає рядок і виводить його навпаки
cat > lab7 <<'SH'                       # створити скрипт
#!/usr/bin/env bash
s="${1-}"                               # рядок-параметр
rev <<<"$s"                             # реверс рядка (через rev)
SH
chmod +x lab7                           # права на виконання

# Пакування (PKN=lab7-v04, VER=1.0)
PKN=lab7-v04; VER=1.0                   # ім'я/версія
rm -rf "$HOME/build/$PKN"               # очистити
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # структури
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # інсталювати у образ
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # опис
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # build
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # install
lab7 "linux" || true                    # тест: "linux" → "xunil"
sudo dpkg -r $PKN                      # remove

```
# ========================= ВАРІАНТ 5 =========================
```bash

# Підготовка
sudo apt update                         # оновити індекси
apt list --installed                    # встановлені пакети
sudo apt install -y mc                  # встановити mc
mc --version                            # версія
ldd "$(command -v mc)"                  # залежності

# A5: Читає зі stdin, друкує без пробілів
cat > lab7 <<'SH'                       # створити скрипт
#!/usr/bin/env bash
tr -d ' '                               # прибрати всі пробіли зі стандартного вводу
SH
chmod +x lab7                           # зробити виконуваним

# Пакування (PKN=lab7-v05, VER=1.0)
PKN=lab7-v05; VER=1.0                   # ім'я/версія
rm -rf "$HOME/build/$PKN"               # чистка
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # директорії
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # встановити скрипт
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # control
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # збірка
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # інсталяція
echo "a b c" | lab7 || true             # тест: "abc"
sudo dpkg -r $PKN                      # видалення

```
# ========================= ВАРІАНТ 6 =========================
```bash

# Підготовка
sudo apt update                         # апдейт індексів
apt list --installed                    # список встановлених
sudo apt install -y mc                  # mc
mc --version                            # версія
ldd "$(command -v mc)"                  # dlibs

# A6: Виводить поточну дату
cat > lab7 <<'SH'                       # скрипт
#!/usr/bin/env bash
date +"%Y-%m-%d"                        # ISO-дата
SH
chmod +x lab7                           # виконуваний

# Пакування (PKN=lab7-v06, VER=1.0)
PKN=lab7-v06; VER=1.0
rm -rf "$HOME/build/$PKN"               # чистка
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # дерева
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # інсталяція у образ
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # метадані
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # build
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # install
lab7 || true                           # тест: дата
sudo dpkg -r $PKN                      # remove

```
# ========================= ВАРІАНТ 7 =========================
```bash

# Підготовка
sudo apt update                         # оновити індекси
apt list --installed                    # список установлених
sudo apt install -y mc                  # інсталяція mc
mc --version                            # версія
ldd "$(command -v mc)"                  # залежності

# A7: Виводить поточний час
cat > lab7 <<'SH'                       # створити скрипт
#!/usr/bin/env bash
date +"%H:%M:%S"                        # поточний час у форматі HH:MM:SS
SH
chmod +x lab7                           # зробити виконуваним

# Пакування (PKN=lab7-v07, VER=1.0)
PKN=lab7-v07; VER=1.0
rm -rf "$HOME/build/$PKN"               # чистка
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # структура
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # інсталяція у образ
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # control
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # зібрати .deb
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # встановити
lab7 || true                           # тест: час
sudo dpkg -r $PKN                      # видалити

```
# ========================= ВАРІАНТ 8 =========================
```bash

# Підготовка
sudo apt update                         # оновити
apt list --installed                    # перелік встановлених
sudo apt install -y mc                  # mc
mc --version                            # версія
ldd "$(command -v mc)"                  # залежності

# A8: Виводить 'ubuntu' 3 рази
cat > lab7 <<'SH'                       # створити скрипт
#!/usr/bin/env bash
for _ in 1 2 3; do echo ubuntu; done    # три рази надрукувати "ubuntu"
SH
chmod +x lab7                           # виконуваний

# Пакування (PKN=lab7-v08, VER=1.0)
PKN=lab7-v08; VER=1.0
rm -rf "$HOME/build/$PKN"               # почистити
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # підготувати структуру
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # скопіювати скрипт
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # опис пакета
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # build .deb
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # install
lab7 || true                           # тест
sudo dpkg -r $PKN                      # remove

```
# ========================= ВАРІАНТ 9 =========================
```bash

# Підготовка
sudo apt update                         # оновити індекси
apt list --installed                    # список пакунків
sudo apt install -y mc                  # інсталяція mc
mc --version                            # версія
ldd "$(command -v mc)"                  # список dlibs

# A9: Приймає рядок, рахує кількість літер 'a'
cat > lab7 <<'SH'                       # створити скрипт
#!/usr/bin/env bash
s="${1-}"                               # рядок
grep -o 'a' <<<"$s" | wc -l             # порахувати 'a'
SH
chmod +x lab7                           # виконуваний

# Пакування (PKN=lab7-v09, VER=1.0)
PKN=lab7-v09; VER=1.0
rm -rf "$HOME/build/$PKN"               # чистка
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # структури
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # покласти скрипт
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # control
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # збірка
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # інсталяція
lab7 "abracadabra" || true              # тест → 5
sudo dpkg -r $PKN                      # видалити

```
# ========================= ВАРІАНТ 10 =========================
```bash

# Підготовка
sudo apt update                         # оновлення
apt list --installed                    # встановлені
sudo apt install -y mc                  # mc
mc --version                            # версія
ldd "$(command -v mc)"                  # dlibs

# A10: Приймає n, виводить n..1
cat > lab7 <<'SH'                       # створити скрипт
#!/usr/bin/env bash
n="${1?Usage: lab7 <n>}"                # обов'язковий аргумент
seq "$n" -1 1 | paste -sd' ' -          # n n-1 ... 1 у рядок
SH
chmod +x lab7                           # зробити виконуваним

# Пакування (PKN=lab7-v10, VER=1.0)
PKN=lab7-v10; VER=1.0
rm -rf "$HOME/build/$PKN"               # чистка
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # каталоги
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # інсталяція у образ
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # метадані
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # зібрати
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # встановити
lab7 7 || true                         # тест: 7 6 5 4 3 2 1
sudo dpkg -r $PKN                      # прибрати

```
# ========================= ВАРІАНТ 11 =========================
```bash

# Підготовка
sudo apt update                         # апдейт
apt list --installed                    # список
sudo apt install -y mc                  # mc
mc --version                            # версія
ldd "$(command -v mc)"                  # dlibs

# A11: Рядок навпаки (ще раз)
cat > lab7 <<'SH'                       # скрипт
#!/usr/bin/env bash
s="${1-}"                               # параметр
rev <<<"$s"                             # реверс
SH
chmod +x lab7                           # виконуваний

# Пакування (PKN=lab7-v11, VER=1.0)
PKN=lab7-v11; VER=1.0
rm -rf "$HOME/build/$PKN"               # чистка
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # дерево
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # скрипт у bin
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # метадані
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # збірка
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # інсталяція
lab7 "abc" || true                     # тест → "cba"
sudo dpkg -r $PKN                      # деінсталяція

```
# ========================= ВАРІАНТ 12 =========================
```bash

# Підготовка
sudo apt update                         # оновити
apt list --installed                    # встановлені
sudo apt install -y mc                  # mc
mc --version                            # версія
ldd "$(command -v mc)"                  # dlibs

# A12: stdin без пробілів (ще раз)
cat > lab7 <<'SH'                       # скрипт
#!/usr/bin/env bash
tr -d ' '                               # прибрати пробіли з STDIN
SH
chmod +x lab7                           # виконуваний

# Пакування (PKN=lab7-v12, VER=1.0)
PKN=lab7-v12; VER=1.0
rm -rf "$HOME/build/$PKN"               # чистка
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # каталоги
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # інсталювати
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # control
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKK/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # ← УВАГА: якщо помилишся в $PKK — виправити на $PKN
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # встановити
echo "a b   c" | lab7 || true            # тест → "a

```
# ========================= ВАРІАНТ 13 =========================
``` bash

# Підготовка
sudo apt update                         # апдейт індексів
apt list --installed                    # інстальовані пакети
sudo apt install -y mc                  # mc
mc --version                            # версія
ldd "$(command -v mc)"                  # залежності

# A13: Поточний місяць літерами
cat > lab7 <<'SH'                       # скрипт
#!/usr/bin/env bash
date +%B                                 # надрукувати назву місяця (локалізовано)
SH
chmod +x lab7                           # виконуваний

# Пакування (PKN=lab7-v13, VER=1.0)
PKN=lab7-v13; VER=1.0
rm -rf "$HOME/build/$PKN"               # чистка
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # дерево
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # скопіювати скрипт
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # control
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # збірка
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # інсталяція
lab7 || true                           # тест → місяць
sudo dpkg -r $PKN                      # видалення

```
# ========================= ВАРІАНТ 14 =========================
``` bash

# Підготовка
sudo apt update                         # оновити
apt list --installed                    # показати встановлені
sudo apt install -y mc                  # інсталювати mc
mc --version                            # версія
ldd "$(command -v mc)"                  # залежності

# A14: hostname
cat > lab7 <<'SH'                       # скрипт
#!/usr/bin/env bash
hostname                                # надрукувати ім'я хоста
SH
chmod +x lab7                           # виконуваний

# Пакування (PKN=lab7-v14, VER=1.0)
PKN=lab7-v14; VER=1.0
rm -rf "$HOME/build/$PKN"               # чистка
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # каталоги
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # інсталювати в образ
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # метадані
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # build
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # install
lab7 || true                           # тест → hostname
sudo dpkg -r $PKN                      # remove

```
# ========================= ВАРІАНТ 15 =========================
``` bash

# Підготовка
sudo apt update                         # апдейт індексів
apt list --installed                    # інстальовані
sudo apt install -y mc                  # mc
mc --version                            # версія
ldd "$(command -v mc)"                  # dlibs

# A15: Приймає число n, виводить n^2
cat > lab7 <<'SH'                       # скрипт
#!/usr/bin/env bash
n="${1?Usage: lab7 <n>}"                # обов'язковий аргумент
echo $(( n * n ))                       # квадрат числа
SH
chmod +x lab7                           # виконуваний

# Пакування (PKN=lab7-v15, VER=1.0)
PKN=lab7-v15; VER=1.0
rm -rf "$HOME/build/$PKN"               # чистка
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"  # структура
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"                # встановити у образ
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF                             # control
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"  # збірка
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"                             # інсталяція
lab7 12 || true                        # тест → 144
sudo dpkg -r $PKN                      # видалення

```

---

# Перелік команд і опцій, що використовуються в ЛР №7 (і що вони роблять)

## Пакетний менеджер APT
- `sudo apt update` — оновлює **індекси репозиторіїв** (список доступних пакунків і версій).
- `apt list --installed` — перелік **встановлених** пакунків.
- `sudo apt install -y mc` — встановлює пакунок `mc`; `-y` автоматично підтверджує.
- `mc --version` — показує версію встановленого `mc`.

## Пошук виконуваних файлів та залежностей
- `` command -v mc `` — повний шлях до виконуваного файлу `mc` (або порожньо, якщо нема).
- `ldd "$(command -v mc)"` — список **динамічних бібліотек**, від яких залежить виконуваний файл.

## Створення скриптів
- `cat > lab7 <<'SH' ... SH` — створює файл `lab7` з вмістом **через here-doc** (у лапках — *без* підстановок).
- `chmod +x lab7` — робить файл **виконуваним**.
- `install -m 0755 lab7 /usr/local/bin/lab7` — копіює з правами 0755 (власник rwx, інші rx); надійніше за `cp` для інсталяції.
