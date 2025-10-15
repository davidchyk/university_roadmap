#!/usr/bin/env bash
# taskNo4_main.sh - спершу видаляє порожні файли, потім порожні директорії (рекурсивно)
set -euo pipefail

DIR="${1:-.}"
[[ -d $DIR ]] || { echo "Помилка: '$DIR' не існує або не є директорією" >&2; exit 1; }

printf "Цільова директорія: %s\n" "$DIR"
printf "Крок 1: Знаходимо порожні файли\n"
find -P "$DIR" -type f -empty -print -delete || true

printf "\nКрок 2: Знаходимо порожні директорії\n"
find -P "$DIR" -depth -type d -empty -print -delete || true

echo -e "\nГотово: видалені порожні директорії"