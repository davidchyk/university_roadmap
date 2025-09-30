# ЛР №9 — LVM, файлові системи, loop-пристрої (усі варіанти)

# Підготовка (для всіх варіантів)
```bash
# створення файлів потрібного розміру (псевдо-дисків)
dd if=/dev/zero of=diskX.img bs=1M count=<SIZE_MB>

# прив’язка до loop-пристрою
sudo losetup /dev/loopN diskX.img

# створення фізичних томів
sudo pvcreate /dev/loopN ...

# створення групи томів (VG)
sudo vgcreate vg_lab /dev/loopN ...

# створення логічних томів (LV)
sudo lvcreate -n <lv_name> -L <size>M vg_lab

# створення файлової системи
sudo mkfs.<fstype> /dev/vg_lab/<lv_name>

# монтування
sudo mkdir -p /mnt/<lv_name>
sudo mount /dev/vg_lab/<lv_name> /mnt/<lv_name>
```
# ========================= ВАРІАНТ 1 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1000
dd if=/dev/zero of=disk2.img bs=1M count=1000
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img

sudo pvcreate /dev/loop1 /dev/loop2
sudo vgcreate vg_lab /dev/loop1 /dev/loop2

sudo lvcreate -n test -L 1200M vg_lab
sudo lvcreate -n newdata -L 300M vg_lab

sudo mkfs.ext4 /dev/vg_lab/test
sudo mkfs.reiserfs /dev/vg_lab/newdata
```
# ========================= ВАРІАНТ 2 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1000
dd if=/dev/zero of=disk2.img bs=1M count=500
dd if=/dev/zero of=disk3.img bs=1M count=500
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img
sudo losetup /dev/loop3 disk3.img

sudo pvcreate /dev/loop1 /dev/loop2 /dev/loop3
sudo vgcreate vg_lab /dev/loop1 /dev/loop2 /dev/loop3

sudo lvcreate -n data1 -L 550M vg_lab
sudo lvcreate -n data2 -L 550M vg_lab
sudo lvcreate -n data3 -L 550M vg_lab

sudo mkfs.ext4 /dev/vg_lab/data1
sudo mkfs.ext4 /dev/vg_lab/data2
sudo mkfs.ext4 /dev/vg_lab/data3
```
# ========================= ВАРІАНТ 3 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=300
dd if=/dev/zero of=disk2.img bs=1M count=300
dd if=/dev/zero of=disk3.img bs=1M count=1200
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img
sudo losetup /dev/loop3 disk3.img

sudo pvcreate /dev/loop1 /dev/loop2 /dev/loop3
sudo vgcreate vg_lab /dev/loop1 /dev/loop2 /dev/loop3

sudo lvcreate -n c1 -L 400M vg_lab
sudo lvcreate -n c2 -L 400M vg_lab
sudo lvcreate -n c3 -L 400M vg_lab
sudo lvcreate -n c4 -L 400M vg_lab

sudo mkfs.ext3 /dev/vg_lab/c1
sudo mkfs.ext3 /dev/vg_lab/c2
sudo mkfs.ext3 /dev/vg_lab/c3
sudo mkfs.ext3 /dev/vg_lab/c4
```
# ========================= ВАРІАНТ 4 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=500
dd if=/dev/zero of=disk2.img bs=1M count=1500
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img

sudo pvcreate /dev/loop1 /dev/loop2
sudo vgcreate vg_lab /dev/loop1 /dev/loop2

sudo lvcreate -n test1 -L 900M vg_lab
sudo lvcreate -n test2 -L 900M vg_lab

sudo mkfs.ext4 /dev/vg_lab/test1
sudo mkfs.msdos /dev/vg_lab/test2
```
# ========================= ВАРІАНТ 5 =========================
``` bash

dd if=/dev/zero of=disk1.img bs=1M count=700
dd if=/dev/zero of=disk2.img bs=1M count=700
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img

sudo pvcreate /dev/loop1 /dev/loop2
sudo vgcreate vg_lab /dev/loop1 /dev/loop2

sudo lvcreate -n d1 -L 500M vg_lab
sudo lvcreate -n d2 -L 500M vg_lab
sudo lvcreate -n d3 -L 300M vg_lab

sudo mkfs.ext4 /dev/vg_lab/d1
sudo mkfs.ext4 /dev/vg_lab/d2
sudo mkfs.ext4 /dev/vg_lab/d3
```
# ========================= ВАРІАНТ 6 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1000
dd if=/dev/zero of=disk2.img bs=1M count=500
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img

sudo pvcreate /dev/loop1 /dev/loop2
sudo vgcreate vg_lab /dev/loop1 /dev/loop2

sudo lvcreate -n x1 -L 700M vg_lab
sudo lvcreate -n x2 -L 700M vg_lab

sudo mkfs.reiserfs /dev/vg_lab/x1
sudo mkfs.reiserfs /dev/vg_lab/x2
```
# ========================= ВАРІАНТ 7 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1500
dd if=/dev/zero of=disk2.img bs=1M count=1000
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img

sudo pvcreate /dev/loop1 /dev/loop2
sudo vgcreate vg_lab /dev/loop1 /dev/loop2

sudo lvcreate -n a1 -L 600M vg_lab
sudo lvcreate -n a2 -L 600M vg_lab
sudo lvcreate -n a3 -L 600M vg_lab
sudo lvcreate -n a4 -L 600M vg_lab

sudo mkfs.ext4 /dev/vg_lab/a1
sudo mkfs.ext4 /dev/vg_lab/a2
sudo mkfs.ext4 /dev/vg_lab/a3
sudo mkfs.ext4 /dev/vg_lab/a4
```
# ========================= ВАРІАНТ 8 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=2000
sudo losetup /dev/loop1 disk1.img

sudo pvcreate /dev/loop1
sudo vgcreate vg_lab /dev/loop1

sudo lvcreate -n home -L 800M vg_lab
sudo lvcreate -n var -L 800M vg_lab
sudo lvcreate -n tmp -L 200M vg_lab

sudo mkfs.ext4 /dev/vg_lab/home
sudo mkfs.ext4 /dev/vg_lab/var
sudo mkfs.msdos /dev/vg_lab/tmp
```
# ========================= ВАРІАНТ 9 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=500
dd if=/dev/zero of=disk2.img bs=1M count=500
dd if=/dev/zero of=disk3.img bs=1M count=500
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img
sudo losetup /dev/loop3 disk3.img

sudo pvcreate /dev/loop1 /dev/loop2 /dev/loop3
sudo vgcreate vg_lab /dev/loop1 /dev/loop2 /dev/loop3

sudo lvcreate -n l1 -L 400M vg_lab
sudo lvcreate -n l2 -L 400M vg_lab
sudo lvcreate -n l3 -L 400M vg_lab

sudo mkfs.ext3 /dev/vg_lab/l1
sudo mkfs.ext3 /dev/vg_lab/l2
sudo mkfs.ext3 /dev/vg_lab/l3
```
# ========================= ВАРІАНТ 10 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=600
dd if=/dev/zero of=disk2.img bs=1M count=600
dd if=/dev/zero of=disk3.img bs=1M count=600
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img
sudo losetup /dev/loop3 disk3.img

sudo pvcreate /dev/loop1 /dev/loop2 /dev/loop3
sudo vgcreate vg_lab /dev/loop1 /dev/loop2 /dev/loop3

sudo lvcreate -n h1 -L 500M vg_lab
sudo lvcreate -n h2 -L 500M vg_lab
sudo lvcreate -n h3 -L 500M vg_lab

sudo mkfs.ext4 /dev/vg_lab/h1
sudo mkfs.reiserfs /dev/vg_lab/h2
sudo mkfs.reiserfs /dev/vg_lab/h3
```
# ========================= ВАРІАНТ 11 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=800
dd if=/dev/zero of=disk2.img bs=1M count=800
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img

sudo pvcreate /dev/loop1 /dev/loop2
sudo vgcreate vg_lab /dev/loop1 /dev/loop2

sudo lvcreate -n d11 -L 600M vg_lab
sudo lvcreate -n d12 -L 600M vg_lab
sudo lvcreate -n d13 -L 200M vg_lab

sudo mkfs.ext4 /dev/vg_lab/d11
sudo mkfs.ext4 /dev/vg_lab/d12
sudo mkfs.msdos /dev/vg_lab/d13
```
# ========================= ВАРІАНТ 12 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=200
dd if=/dev/zero of=disk2.img bs=1M count=200
dd if=/dev/zero of=disk3.img bs=1M count=200
dd if=/dev/zero of=disk4.img bs=1M count=200
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img
sudo losetup /dev/loop3 disk3.img
sudo losetup /dev/loop4 disk4.img

sudo pvcreate /dev/loop1 /dev/loop2 /dev/loop3 /dev/loop4
sudo vgcreate vg_lab /dev/loop1 /dev/loop2 /dev/loop3 /dev/loop4

sudo lvcreate -n u1 -L 150M vg_lab
sudo lvcreate -n u2 -L 150M vg_lab
sudo lvcreate -n u3 -L 150M vg_lab
sudo lvcreate -n u4 -L 150M vg_lab

sudo mkfs.ext3 /dev/vg_lab/u1
sudo mkfs.ext3 /dev/vg_lab/u2
sudo mkfs.ext3 /dev/vg_lab/u3
sudo mkfs.ext3 /dev/vg_lab/u4
```
# ========================= ВАРІАНТ 13 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1000
dd if=/dev/zero of=disk2.img bs=1M count=1000
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img

sudo pvcreate /dev/loop1 /dev/loop2
sudo vgcreate vg_lab /dev/loop1 /dev/loop2

sudo lvcreate -n test13a -L 700M vg_lab
sudo lvcreate -n test13b -L 700M vg_lab

sudo mkfs.ext4 /dev/vg_lab/test13a
sudo mkfs.reiserfs /dev/vg_lab/test13b
```
# ========================= ВАРІАНТ 14 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1200
dd if=/dev/zero of=disk2.img bs=1M count=800
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img

sudo pvcreate /dev/loop1 /dev/loop2
sudo vgcreate vg_lab /dev/loop1 /dev/loop2

sudo lvcreate -n z1 -L 1000M vg_lab
sudo lvcreate -n z2 -L 800M vg_lab

sudo mkfs.ext4 /dev/vg_lab/z1
sudo mkfs.msdos /dev/vg_lab/z2
```
# ========================= ВАРІАНТ 15 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1500
sudo losetup /dev/loop1 disk1.img

sudo pvcreate /dev/loop1
sudo vgcreate vg_lab /dev/loop1

sudo lvcreate -n single1 -L 700M vg_lab
sudo lvcreate -n single2 -L 700M vg_lab

sudo mkfs.ext4 /dev/vg_lab/single1
sudo mkfs.reiserfs /dev/vg_lab/single2
```

---

# Перелік команд і опцій, що використовуються в ЛР №9 (LVM, файлові системи, loop-пристрої)

## Підготовка (спільна для всіх варіантів)
- `dd if=/dev/zero of=diskX.img bs=1M count=<SIZE_MB>` — створює файл-заглушку (`diskX.img`) розміром `<SIZE_MB>` мегабайт, заповнений нулями (імітація диска).
- `sudo losetup /dev/loopN diskX.img` — прив’язує файл як **loop-пристрій**, щоб працювати з ним як з диском.
- `sudo pvcreate /dev/loopN` — створює **фізичний том (PV)** для LVM.
- `sudo vgcreate vg_lab /dev/loopN ...` — створює **групу томів (VG)** під назвою `vg_lab`.
- `sudo lvcreate -n <lv_name> -L <size>M vg_lab` — створює **логічний том (LV)** з вказаним розміром `<size>` МБ у групі `vg_lab`.
- `sudo mkfs.<fstype> /dev/vg_lab/<lv_name>` — створює **файлову систему** у логічному томі (`ext4`, `ext3`, `reiserfs`, `msdos` тощо).
- `sudo mkdir -p /mnt/<lv_name>` — створює каталог для монтування.
- `sudo mount /dev/vg_lab/<lv_name> /mnt/<lv_name>` — монтує файлову систему в каталог.

## Основні інструменти
- **LVM (Logical Volume Manager):**
  - **PV (Physical Volume)** → фізичний носій (у нас `loop`-файл).
  - **VG (Volume Group)** → об’єднання фізичних томів.
  - **LV (Logical Volume)** → розділ усередині VG, який можна форматувати.

- **mkfs:**
  - `mkfs.ext4` — створює файлову систему **ext4** (стандарт для Linux).
  - `mkfs.ext3` — файлову систему **ext3** (журналювання, попередник ext4).
  - `mkfs.reiserfs` — **ReiserFS** (рідко використовується, але підтримується).
  - `mkfs.msdos` — створює **FAT16/FAT32** файлову систему (сумісна з Windows).