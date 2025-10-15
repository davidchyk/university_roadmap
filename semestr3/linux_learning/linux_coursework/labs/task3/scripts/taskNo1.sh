#!/usr/bin/env bash
# taskNo1.sh - 3 найважчі піддиректорії біля скрипта; вивід за зростанням
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

# Якщо піддиректорій немає - повідомляємо і виходимо
if ! find "$SCRIPT_DIR" -mindepth 1 -maxdepth 1 -type d -print -quit | grep -q .; then
  echo "Поруч зі скриптом немає жодної піддиректорії"
  exit 0
fi

# Ланцюжок: перелік піддиректорій → їх розмір (у байтах) → топ-3 найбільші → відсортовано за зростанням
find "$SCRIPT_DIR" -mindepth 1 -maxdepth 1 -type d -print0 \
| xargs -0 -r du -sB1 \
| sort -n \
| tail -n 3 \
| sort -n \
| while read -r bytes path; do
    if command -v numfmt >/dev/null 2>&1; then
      human=$(numfmt --to=iec --suffix=B --format="%.1f" "$bytes")
    else
      human="${bytes}B"
    fi
    printf "%s\t%s\n" "$human" "${path##*/}"
  done