#!/usr/bin/env bash
# taskNo3.sh - згенерувати 5 додатних чисел, записати у файл, лишити мінімальне
set -euo pipefail

out="${1:-numbers.txt}"

# Згенерувати 5 чисел (1..1e6), показати й записати у файл
nums=$(for _ in {1..5}; do echo $(( (RANDOM<<15 | RANDOM) % 1000000 + 1 )); done)
printf "%s\n" $nums | tee "$out" >/dev/null

echo "Згенеровані числа:"
printf "%s " $nums; echo

# Знайти мінімум і перезаписати файл лише ним
min=$(printf "%s\n" $nums | sort -n | head -n1)
printf "%s\n" "$min" > "$out"

echo "Мінімальне число (залишено у файлі $out): $min"
echo "Вміст файлу після очистки:"
cat "$out"