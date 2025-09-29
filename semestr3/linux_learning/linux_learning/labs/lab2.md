# ЛР №2 — команди для всіх варіантів

# 0) Підготовка файлів
cp /etc/passwd ~/lab2/pass.txt # копія passwd у домашній каталог

# ========== Варіанти ==========

# Варіант 1
```bash
cat test.txt city.txt pass.txt
wc -l test.txt city.txt pass.txt
cut -d: -f1,3 pass.txt
head -n 3 pass.txt
sort city.txt
sed 's/a/b/g' city.txt
grep "Spain" city.txt
split -l 3 city.txt part_
```

# Варіант 2
```bash
cat test.txt city.txt pass.txt
wc -w test.txt city.txt pass.txt
cut -c1-10 pass.txt
tail -n 3 pass.txt
sort -r city.txt
sed 's/in/ /g' city.txt
grep -v "Spain" city.txt
split -l 3 city.txt part_
```

# Варіант 3
```bash
cat test.txt city.txt pass.txt
wc -m test.txt city.txt pass.txt
cut -d: -f1 pass.txt
head -n 10 pass.txt
sort city.txt
sed 's/et/in/g' city.txt
grep -E "Hungary|Austria" city.txt
split -l 3 city.txt part_
```

# Варіант 4
```bash
cat test.txt city.txt pass.txt
wc -l test.txt city.txt pass.txt
cut -d: -f2 pass.txt
tail -n 8 pass.txt
sort -r city.txt
sed 's/et/ /g' city.txt
grep -Ev "Spain|Vienna" city.txt
split -l 3 city.txt part_
```

# Варіант 5
```bash
cat test.txt city.txt pass.txt
wc -w test.txt city.txt pass.txt
cut -c1-3 pass.txt
head -n 5 pass.txt
sort city.txt
sed 's/ /  /g' city.txt
grep -E "^Bu" city.txt
split -l 3 city.txt part_
```

# Варіант 6
```bash
cat test.txt city.txt pass.txt
wc -m test.txt city.txt pass.txt
cut -d: -f4 pass.txt
tail -n 6 pass.txt
sort -r city.txt
sed 's/,/:/g' city.txt
grep "Budapest" city.txt
split -l 3 city.txt part_
```

# Варіант 7
```bash
cat test.txt city.txt pass.txt
wc -l test.txt city.txt pass.txt
cut -d: --complement -f2 pass.txt
head -n 7 pass.txt
sort city.txt
sed 's/ /,/g' city.txt
grep -v "Budapest" city.txt
split -l 3 city.txt part_
```

# Варіант 8
```bash
cat test.txt city.txt pass.txt
wc -w test.txt city.txt pass.txt
cut -d: -f6,1 pass.txt
tail -n 8 pass.txt
sort -r city.txt
sed -e 's/a/X/g' -e 's/b/Y/g' -e 's/c/Z/g' city.txt
grep -E "Hungary|Austria" city.txt
split -l 3 city.txt part_
```

# Варіант 9
```bash
cat test.txt city.txt pass.txt
wc -m test.txt city.txt pass.txt
cut -d: -f1,3 pass.txt
head -n 9 pass.txt
sort city.txt
sed 's/,/,,/g' city.txt
grep -Ev "Spain|Vienna" city.txt
split -l 3 city.txt part_
```

# Варіант 10
```bash
cat test.txt city.txt pass.txt
wc -l test.txt city.txt pass.txt
cut -c2-5 pass.txt
tail -n 10 pass.txt
sort -r city.txt
sed 's/\?/\?!/g' city.txt
grep -E "^Bu" city.txt
split -l 3 city.txt part_
```

# Варіант 11
```bash
cat test.txt city.txt pass.txt
wc -w test.txt city.txt pass.txt
cut -d: --complement -f1 pass.txt
head -n 11 pass.txt
sort city.txt
sed -e 's/a/X/g' -e 's/b/Y/g' -e 's/c/\//g' city.txt
grep -i "austria" city.txt
split -l 3 city.txt part_
```

# Варіант 12
```bash
cat test.txt city.txt pass.txt
wc -m test.txt city.txt pass.txt
cut -d: -f6,7 pass.txt
head -n 12 pass.txt
sort -r city.txt
sed 's/[[:space:]]//g' city.txt
grep -E "^Au" city.txt
split -l 3 city.txt part_
```

# Варіант 13
```bash
cat test.txt city.txt pass.txt
wc -l test.txt city.txt pass.txt
cut -d: -f7,6 pass.txt
tail -n 13 pass.txt
sort city.txt
sed 's/,//g' city.txt
grep -Ev "^B" city.txt
split -l 3 city.txt part_
```

# Варіант 14
```bash
cat test.txt city.txt pass.txt
wc -w test.txt city.txt pass.txt
cut -c10-20 pass.txt
head -n 14 pass.txt
sort -r city.txt
sed 's/b/a/g' city.txt
grep -E '8$' city.txt
split -l 3 city.txt part_
```

# Варіант 15
```bash
cat test.txt city.txt pass.txt
wc -m test.txt city.txt pass.txt
cut -d: -f7 pass.txt
head -n 15 pass.txt
sort city.txt
sed 's/a/\//g' city.txt
grep "Munich" city.txt
split -l 3 city.txt part_
```