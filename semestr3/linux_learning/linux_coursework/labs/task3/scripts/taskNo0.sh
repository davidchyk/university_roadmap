#!/usr/bin/env bash
# taskNo0.sh - якщо $1 > $2 -> показати alias-и; інакше -> показати розмір цього скрипта
set -euo pipefail

[[ $# -eq 2 ]] || { echo "Використання: $0 <int1> <int2>"; exit 1; }
re='^-?[0-9]+$'
[[ $1 =~ $re && $2 =~ $re ]] || { echo "Параметри мають бути цілими числами"; exit 1; }

a=$1 b=$2
me=${BASH_SOURCE[0]}

if (( a > b )); then
  echo "Перший параметр ($a) > другого ($b). Alias-и:"
  alias 2>/dev/null || echo "(alias-и не визначені)"
else
  echo "Перший параметр ($a) <= другого ($b)."
  size=$(stat -c %s -- "$me" 2>/dev/null || wc -c < "$me")
  echo "Файл скрипта: $me"
  echo "Розмір скрипта: $size байт(и)"
fi