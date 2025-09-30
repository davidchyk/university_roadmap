# ЛР №7 — Пакетні менеджери, динамічні бібліотеки, створення пакета (усі варіанти)
> Середовище: Debian/Ubuntu/Mint (apt + dpkg). У кожному варіанті дублюється підготовка.

# ========================= ВАРІАНТ 1 =========================
```bash
# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A1: Вивести 'Hello world'
cat > lab7 <<'SH'
#!/usr/bin/env bash
echo "Hello world"
SH
chmod +x lab7

# Пакування (PKN=lab7-v01, VER=1.0)
PKN=lab7-v01; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 2 =========================
```bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A2: Приймає рядок як параметр, виводить кількість символів
cat > lab7 <<'SH'
#!/usr/bin/env bash
s="${1-}"
echo "${#s}"
SH
chmod +x lab7

# Пакування (PKN=lab7-v02, VER=1.0)
PKN=lab7-v02; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 "mint" || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 3 =========================
```bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A3: Приймає додатне ціле n, виводить 1..n
cat > lab7 <<'SH'
#!/usr/bin/env bash
n="${1?Usage: lab7 <n>}"
seq 1 "$n" | paste -sd' ' -
SH
chmod +x lab7

# Пакування (PKN=lab7-v03, VER=1.0)
PKN=lab7-v03; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 5 || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 4 =========================
```bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A4: Приймає рядок і виводить його навпаки
cat > lab7 <<'SH'
#!/usr/bin/env bash
s="${1-}"
rev <<<"$s"
SH
chmod +x lab7

# Пакування (PKN=lab7-v04, VER=1.0)
PKN=lab7-v04; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 "linux" || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 5 =========================
```bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A5: Читає зі stdin, друкує без пробілів
cat > lab7 <<'SH'
#!/usr/bin/env bash
tr -d ' '
SH
chmod +x lab7

# Пакування (PKN=lab7-v05, VER=1.0)
PKN=lab7-v05; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
echo "a b c" | lab7 || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 6 =========================
```bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A6: Виводить поточну дату
cat > lab7 <<'SH'
#!/usr/bin/env bash
date +"%Y-%m-%d"
SH
chmod +x lab7

# Пакування (PKN=lab7-v06, VER=1.0)
PKN=lab7-v06; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 7 =========================
```bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A7: Виводить поточний час
cat > lab7 <<'SH'
#!/usr/bin/env bash
date +"%H:%M:%S"
SH
chmod +x lab7

# Пакування (PKN=lab7-v07, VER=1.0)
PKN=lab7-v07; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 8 =========================
```bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A8: Виводить 'ubuntu' 3 рази
cat > lab7 <<'SH'
#!/usr/bin/env bash
for _ in 1 2 3; do echo ubuntu; done
SH
chmod +x lab7

# Пакування (PKN=lab7-v08, VER=1.0)
PKN=lab7-v08; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 9 =========================
```bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A9: Приймає рядок, рахує кількість літер 'a'
cat > lab7 <<'SH'
#!/usr/bin/env bash
s="${1-}"
grep -o 'a' <<<"$s" | wc -l
SH
chmod +x lab7

# Пакування (PKN=lab7-v09, VER=1.0)
PKN=lab7-v09; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 "abracadabra" || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 10 =========================
```bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A10: Приймає n, виводить n..1
cat > lab7 <<'SH'
#!/usr/bin/env bash
n="${1?Usage: lab7 <n>}"
seq "$n" -1 1 | paste -sd' ' -
SH
chmod +x lab7

# Пакування (PKN=lab7-v10, VER=1.0)
PKN=lab7-v10; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 7 || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 11 =========================
```bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A11: Рядок навпаки (ще раз)
cat > lab7 <<'SH'
#!/usr/bin/env bash
s="${1-}"
rev <<<"$s"
SH
chmod +x lab7

# Пакування (PKN=lab7-v11, VER=1.0)
PKN=lab7-v11; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 "abc" || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 12 =========================
```bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A12: stdin без пробілів (ще раз)
cat > lab7 <<'SH'
#!/usr/bin/env bash
tr -d ' '
SH
chmod +x lab7

# Пакування (PKN=lab7-v12, VER=1.0)
PKN=lab7-v12; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
echo "a b   c" | lab7 || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 13 =========================
``` bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A13: Поточний місяць літерами
cat > lab7 <<'SH'
#!/usr/bin/env bash
date +%B
SH
chmod +x lab7

# Пакування (PKN=lab7-v13, VER=1.0)
PKN=lab7-v13; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 14 =========================
``` bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A14: hostname
cat > lab7 <<'SH'
#!/usr/bin/env bash
hostname
SH
chmod +x lab7

# Пакування (PKN=lab7-v14, VER=1.0)
PKN=lab7-v14; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 || true
sudo dpkg -r $PKN
```
# ========================= ВАРІАНТ 15 =========================
``` bash

# Підготовка
sudo apt update
apt list --installed
sudo apt install -y mc
mc --version
ldd "$(command -v mc)"

# A15: Приймає число n, виводить n^2
cat > lab7 <<'SH'
#!/usr/bin/env bash
n="${1?Usage: lab7 <n>}"
echo $(( n * n ))
SH
chmod +x lab7

# Пакування (PKN=lab7-v15, VER=1.0)
PKN=lab7-v15; VER=1.0
rm -rf "$HOME/build/$PKN"
mkdir -p "$HOME/build/$PKN/pkg/usr/local/bin" "$HOME/build/$PKN/pkg/DEBIAN"
install -m 0755 lab7 "$HOME/build/$PKN/pkg/usr/local/bin/lab7"
cat > "$HOME/build/$PKN/pkg/DEBIAN/control" <<EOF
Package: $PKN
Version: $VER
Section: utils
Priority: optional
Architecture: all
Maintainer: student <student@example.com>
Description: Lab7 variant package ($PKN)
EOF
dpkg-deb --build "$HOME/build/$PKN/pkg" "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
sudo dpkg -i "$HOME/build/$PKN/${PKN}_${VER}_all.deb"
lab7 12 || true
sudo dpkg -r $PKN
```