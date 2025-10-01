# ЛР №9 — LVM, файлові системи, loop-пристрої (усі варіанти)

# Підготовка (для всіх варіантів)
```bash
dd if=/dev/zero of=diskX.img bs=1M count=<SIZE_MB>   # створюємо файл-образ, який імітує "диск"
sudo losetup /dev/loopN diskX.img                    # прив’язуємо файл до loop-пристрою (блочний інтерфейс)
sudo pvcreate /dev/loopN ...                         # ініціалізуємо як Physical Volume (PV)
sudo vgcreate vg_lab /dev/loopN ...                  # створюємо Volume Group (VG) з кількох PV
sudo lvcreate -n <lv_name> -L <size>M vg_lab         # створюємо Logical Volume (LV) у VG
sudo mkfs.<fstype> /dev/vg_lab/<lv_name>             # форматуємо у вибрану ФС (ext4, ext3, reiserfs, msdos)
sudo mkdir -p /mnt/<lv_name>                         # створюємо точку монтування
sudo mount /dev/vg_lab/<lv_name> /mnt/<lv_name>      # монтуємо для використання

```
# ========================= ВАРІАНТ 1 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1000   # створюємо файл-образ "disk1.img" розміром 1000 МБ
dd if=/dev/zero of=disk2.img bs=1M count=1000   # створюємо файл-образ "disk2.img" розміром 1000 МБ

sudo losetup /dev/loop1 disk1.img               # прив’язуємо "disk1.img" до loop-пристрою /dev/loop1
sudo losetup /dev/loop2 disk2.img               # прив’язуємо "disk2.img" до loop-пристрою /dev/loop2

sudo pvcreate /dev/loop1 /dev/loop2             # ініціалізуємо обидва loop-диски як Physical Volumes
sudo vgcreate vg_lab /dev/loop1 /dev/loop2      # створюємо Volume Group "vg_lab" з двох PV

sudo lvcreate -n test -L 1200M vg_lab           # створюємо логічний том "test" розміром 1200 МБ
sudo lvcreate -n newdata -L 300M vg_lab         # створюємо логічний том "newdata" розміром 300 МБ

sudo mkfs.ext4 /dev/vg_lab/test                 # форматуємо LV "test" у файлову систему ext4
sudo mkfs.reiserfs /dev/vg_lab/newdata          # форматуємо LV "newdata" у файлову систему reiserfs


```
# ========================= ВАРІАНТ 2 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1000   # створюємо образ на 1000 МБ
dd if=/dev/zero of=disk2.img bs=1M count=500    # створюємо образ на 500 МБ
dd if=/dev/zero of=disk3.img bs=1M count=500    # створюємо образ на 500 МБ

sudo losetup /dev/loop1 disk1.img               # прив’язуємо disk1 до /dev/loop1
sudo losetup /dev/loop2 disk2.img               # прив’язуємо disk2 до /dev/loop2
sudo losetup /dev/loop3 disk3.img               # прив’язуємо disk3 до /dev/loop3

sudo pvcreate /dev/loop1 /dev/loop2 /dev/loop3  # ініціалізуємо три PV
sudo vgcreate vg_lab /dev/loop1 /dev/loop2 /dev/loop3  # створюємо VG з 3 дисків

sudo lvcreate -n data1 -L 550M vg_lab           # LV "data1" розміром 550 МБ
sudo lvcreate -n data2 -L 550M vg_lab           # LV "data2" розміром 550 МБ
sudo lvcreate -n data3 -L 550M vg_lab           # LV "data3" розміром 550 МБ

sudo mkfs.ext4 /dev/vg_lab/data1                # форматування LV data1 у ext4
sudo mkfs.ext4 /dev/vg_lab/data2                # форматування LV data2 у ext4
sudo mkfs.ext4 /dev/vg_lab/data3                # форматування LV data3 у ext4


```
# ========================= ВАРІАНТ 3 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=300    # образ на 300 МБ
dd if=/dev/zero of=disk2.img bs=1M count=300    # образ на 300 МБ
dd if=/dev/zero of=disk3.img bs=1M count=1200   # образ на 1200 МБ

sudo losetup /dev/loop1 disk1.img               # прив’язуємо disk1 до /dev/loop1
sudo losetup /dev/loop2 disk2.img               # прив’язуємо disk2 до /dev/loop2
sudo losetup /dev/loop3 disk3.img               # прив’язуємо disk3 до /dev/loop3

sudo pvcreate /dev/loop1 /dev/loop2 /dev/loop3  # створюємо 3 PV
sudo vgcreate vg_lab /dev/loop1 /dev/loop2 /dev/loop3 # створюємо VG з 3 PV

sudo lvcreate -n c1 -L 400M vg_lab              # логічний том c1 (400 МБ)
sudo lvcreate -n c2 -L 400M vg_lab              # логічний том c2 (400 МБ)
sudo lvcreate -n c3 -L 400M vg_lab              # логічний том c3 (400 МБ)
sudo lvcreate -n c4 -L 400M vg_lab              # логічний том c4 (400 МБ)

sudo mkfs.ext3 /dev/vg_lab/c1                   # форматування c1 у ext3
sudo mkfs.ext3 /dev/vg_lab/c2                   # форматування c2 у ext3
sudo mkfs.ext3 /dev/vg_lab/c3                   # форматування c3 у ext3
sudo mkfs.ext3 /dev/vg_lab/c4                   # форматування c4 у ext3


```
# ========================= ВАРІАНТ 4 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=500    # образ на 500 МБ
dd if=/dev/zero of=disk2.img bs=1M count=1500   # образ на 1500 МБ

sudo losetup /dev/loop1 disk1.img               # disk1 → loop1
sudo losetup /dev/loop2 disk2.img               # disk2 → loop2

sudo pvcreate /dev/loop1 /dev/loop2             # створюємо PV з 2 loop-дисків
sudo vgcreate vg_lab /dev/loop1 /dev/loop2      # створюємо VG "vg_lab"

sudo lvcreate -n test1 -L 900M vg_lab           # логічний том test1 (900 МБ)
sudo lvcreate -n test2 -L 900M vg_lab           # логічний том test2 (900 МБ)

sudo mkfs.ext4 /dev/vg_lab/test1                # форматування test1 у ext4
sudo mkfs.msdos /dev/vg_lab/test2               # форматування test2 у FAT32 (msdos)


```
# ========================= ВАРІАНТ 5 =========================
``` bash

dd if=/dev/zero of=disk1.img bs=1M count=700    # створюємо образ 700 МБ
dd if=/dev/zero of=disk2.img bs=1M count=700    # створюємо ще один образ 700 МБ

sudo losetup /dev/loop1 disk1.img               # disk1 → loop1
sudo losetup /dev/loop2 disk2.img               # disk2 → loop2

sudo pvcreate /dev/loop1 /dev/loop2             # створюємо два PV
sudo vgcreate vg_lab /dev/loop1 /dev/loop2      # створюємо VG з двох PV

sudo lvcreate -n d1 -L 500M vg_lab              # LV d1 (500 МБ)
sudo lvcreate -n d2 -L 500M vg_lab              # LV d2 (500 МБ)
sudo lvcreate -n d3 -L 300M vg_lab              # LV d3 (300 МБ)

sudo mkfs.ext4 /dev/vg_lab/d1                   # форматування d1 у ext4
sudo mkfs.ext4 /dev/vg_lab/d2                   # форматування d2 у ext4
sudo mkfs.ext4 /dev/vg_lab/d3                   # форматування d3 у ext4


```
# ========================= ВАРІАНТ 6 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1000   # образ 1000 МБ
dd if=/dev/zero of=disk2.img bs=1M count=500    # образ 500 МБ

sudo losetup /dev/loop1 disk1.img               # disk1 → loop1
sudo losetup /dev/loop2 disk2.img               # disk2 → loop2

sudo pvcreate /dev/loop1 /dev/loop2             # створюємо PV
sudo vgcreate vg_lab /dev/loop1 /dev/loop2      # створюємо VG з двох PV

sudo lvcreate -n x1 -L 700M vg_lab              # LV x1 (700 МБ)
sudo lvcreate -n x2 -L 700M vg_lab              # LV x2 (700 МБ)

sudo mkfs.reiserfs /dev/vg_lab/x1               # форматування x1 у reiserfs
sudo mkfs.reiserfs /dev/vg_lab/x2               # форматування x2 у reiserfs


```
# ========================= ВАРІАНТ 7 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1500   # образ 1500 МБ
dd if=/dev/zero of=disk2.img bs=1M count=1000   # образ 1000 МБ

sudo losetup /dev/loop1 disk1.img               # disk1 → loop1
sudo losetup /dev/loop2 disk2.img               # disk2 → loop2

sudo pvcreate /dev/loop1 /dev/loop2             # створюємо PV
sudo vgcreate vg_lab /dev/loop1 /dev/loop2      # створюємо VG

sudo lvcreate -n a1 -L 600M vg_lab              # LV a1 (600 МБ)
sudo lvcreate -n a2 -L 600M vg_lab              # LV a2 (600 МБ)
sudo lvcreate -n a3 -L 600M vg_lab              # LV a3 (600 МБ)
sudo lvcreate -n a4 -L 600M vg_lab              # LV a4 (600 МБ)

sudo mkfs.ext4 /dev/vg_lab/a1                   # формат ext4
sudo mkfs.ext4 /dev/vg_lab/a2
sudo mkfs.ext4 /dev/vg_lab/a3
sudo mkfs.ext4 /dev/vg_lab/a4

```
# ========================= ВАРІАНТ 8 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=2000   # образ 2000 МБ

sudo losetup /dev/loop1 disk1.img               # disk1 → loop1

sudo pvcreate /dev/loop1                        # створюємо PV
sudo vgcreate vg_lab /dev/loop1                 # створюємо VG з одного PV

sudo lvcreate -n home -L 800M vg_lab            # LV home (800 МБ)
sudo lvcreate -n var -L 800M vg_lab             # LV var (800 МБ)
sudo lvcreate -n tmp -L 200M vg_lab             # LV tmp (200 МБ)

sudo mkfs.ext4 /dev/vg_lab/home                 # ext4
sudo mkfs.ext4 /dev/vg_lab/var
sudo mkfs.msdos /dev/vg_lab/tmp                 # FAT32


```
# ========================= ВАРІАНТ 9 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=500    # образ 500 МБ
dd if=/dev/zero of=disk2.img bs=1M count=500    # образ 500 МБ
dd if=/dev/zero of=disk3.img bs=1M count=500    # образ 500 МБ

sudo losetup /dev/loop1 disk1.img               # disk1 → loop1
sudo losetup /dev/loop2 disk2.img               # disk2 → loop2
sudo losetup /dev/loop3 disk3.img               # disk3 → loop3

sudo pvcreate /dev/loop1 /dev/loop2 /dev/loop3  # створюємо 3 PV
sudo vgcreate vg_lab /dev/loop1 /dev/loop2 /dev/loop3 # створюємо VG

sudo lvcreate -n l1 -L 400M vg_lab              # LV l1 (400 МБ)
sudo lvcreate -n l2 -L 400M vg_lab              # LV l2 (400 МБ)
sudo lvcreate -n l3 -L 400M vg_lab              # LV l3 (400 МБ)

sudo mkfs.ext3 /dev/vg_lab/l1                   # формат ext3
sudo mkfs.ext3 /dev/vg_lab/l2
sudo mkfs.ext3 /dev/vg_lab/l3


```
# ========================= ВАРІАНТ 10 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=600    # образ 600 МБ
dd if=/dev/zero of=disk2.img bs=1M count=600    # образ 600 МБ
dd if=/dev/zero of=disk3.img bs=1M count=600    # образ 600 МБ

sudo losetup /dev/loop1 disk1.img               # disk1 → loop1
sudo losetup /dev/loop2 disk2.img               # disk2 → loop2
sudo losetup /dev/loop3 disk3.img               # disk3 → loop3

sudo pvcreate /dev/loop1 /dev/loop2 /dev/loop3  # створюємо PV
sudo vgcreate vg_lab /dev/loop1 /dev/loop2 /dev/loop3 # створюємо VG

sudo lvcreate -n h1 -L 500M vg_lab              # LV h1 (500 МБ)
sudo lvcreate -n h2 -L 500M vg_lab              # LV h2 (500 МБ)
sudo lvcreate -n h3 -L 500M vg_lab              # LV h3 (500 МБ)

sudo mkfs.ext4 /dev/vg_lab/h1                   # формат ext4
sudo mkfs.reiserfs /dev/vg_lab/h2               # формат reiserfs
sudo mkfs.reiserfs /dev/vg_lab/h3               # формат reiserfs


```
# ========================= ВАРІАНТ 11 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=800    # образ 800 МБ
dd if=/dev/zero of=disk2.img bs=1M count=800    # образ 800 МБ

sudo losetup /dev/loop1 disk1.img               # disk1 → loop1
sudo losetup /dev/loop2 disk2.img               # disk2 → loop2

sudo pvcreate /dev/loop1 /dev/loop2             # створюємо PV
sudo vgcreate vg_lab /dev/loop1 /dev/loop2      # створюємо VG

sudo lvcreate -n d11 -L 600M vg_lab             # LV d11 (600 МБ)
sudo lvcreate -n d12 -L 600M vg_lab             # LV d12 (600 МБ)
sudo lvcreate -n d13 -L 200M vg_lab             # LV d13 (200 МБ)

sudo mkfs.ext4 /dev/vg_lab/d11                  # ext4
sudo mkfs.ext4 /dev/vg_lab/d12
sudo mkfs.msdos /dev/vg_lab/d13                 # FAT32


```
# ========================= ВАРІАНТ 12 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=200    # образ 200 МБ
dd if=/dev/zero of=disk2.img bs=1M count=200    # образ 200 МБ
dd if=/dev/zero of=disk3.img bs=1M count=200    # образ 200 МБ
dd if=/dev/zero of=disk4.img bs=1M count=200    # образ 200 МБ

sudo losetup /dev/loop1 disk1.img               # loop1
sudo losetup /dev/loop2 disk2.img               # loop2
sudo losetup /dev/loop3 disk3.img               # loop3
sudo losetup /dev/loop4 disk4.img               # loop4

sudo pvcreate /dev/loop1 /dev/loop2 /dev/loop3 /dev/loop4 # створюємо PV
sudo vgcreate vg_lab /dev/loop1 /dev/loop2 /dev/loop3 /dev/loop4 # VG

sudo lvcreate -n u1 -L 150M vg_lab              # LV u1
sudo lvcreate -n u2 -L 150M vg_lab              # LV u2
sudo lvcreate -n u3 -L 150M vg_lab              # LV u3
sudo lvcreate -n u4 -L 150M vg_lab              # LV u4

sudo mkfs.ext3 /dev/vg_lab/u1                   # ext3
sudo mkfs.ext3 /dev/vg_lab/u2
sudo mkfs.ext3 /dev/vg_lab/u3
sudo mkfs.ext3 /dev/vg_lab/u4

```
# ========================= ВАРІАНТ 13 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1000   # образ 1000 МБ
dd if=/dev/zero of=disk2.img bs=1M count=1000   # образ 1000 МБ

sudo losetup /dev/loop1 disk1.img               # loop1
sudo losetup /dev/loop2 disk2.img               # loop2

sudo pvcreate /dev/loop1 /dev/loop2             # створюємо PV
sudo vgcreate vg_lab /dev/loop1 /dev/loop2      # створюємо VG

sudo lvcreate -n test13a -L 700M vg_lab         # LV test13a
sudo lvcreate -n test13b -L 700M vg_lab         # LV test13b

sudo mkfs.ext4 /dev/vg_lab/test13a              # ext4
sudo mkfs.reiserfs /dev/vg_lab/test13b          # reiserfs

```
# ========================= ВАРІАНТ 14 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1200   # образ 1200 МБ
dd if=/dev/zero of=disk2.img bs=1M count=800    # образ 800 МБ

sudo losetup /dev/loop1 disk1.img               # loop1
sudo losetup /dev/loop2 disk2.img               # loop2

sudo pvcreate /dev/loop1 /dev/loop2             # PV
sudo vgcreate vg_lab /dev/loop1 /dev/loop2      # VG

sudo lvcreate -n z1 -L 1000M vg_lab             # LV z1
sudo lvcreate -n z2 -L 800M vg_lab              # LV z2

sudo mkfs.ext4 /dev/vg_lab/z1                   # ext4
sudo mkfs.msdos /dev/vg_lab/z2                  # FAT32

```
# ========================= ВАРІАНТ 15 =========================
```bash

dd if=/dev/zero of=disk1.img bs=1M count=1500   # образ 1500 МБ

sudo losetup /dev/loop1 disk1.img               # loop1

sudo pvcreate /dev/loop1                        # створюємо PV
sudo vgcreate vg_lab /dev/loop1                 # створюємо VG

sudo lvcreate -n single1 -L 700M vg_lab         # LV single1
sudo lvcreate -n single2 -L 700M vg_lab         # LV single2

sudo mkfs.ext4 /dev/vg_lab/single1              # ext4
sudo mkfs.reiserfs /dev/vg_lab/single2          # reiserfs

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