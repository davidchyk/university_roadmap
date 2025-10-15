#!/usr/bin/env bash
# taskNo2.sh - пройтись по вмісту каталогу
set -euo pipefail

TARGET_DIR="${1:-.}"
[[ -d "$TARGET_DIR" ]] || { echo "Помилка: це не директорія: $TARGET_DIR" >&2; exit 1; }

# Перебір лише першого рівня (включно з прихованими). Отримаємо БАЗОВІ імена через %P.
while IFS= read -r -d '' name; do
  path="$TARGET_DIR/$name"

  if [[ -d "$path" ]]; then
    printf "%s є директорією\n" "$name"

  elif [[ -f "$path" || ( -L "$path" && ! -d "$path" ) ]]; then
    dest="$TARGET_DIR/${name}_dir"
    mkdir -p -- "$dest"

    target="$dest/$name"
    if [[ -e "$target" ]]; then
      i=1
      while [[ -e "$dest/${name}.dup${i}" ]]; do ((i++)); done
      target="$dest/${name}.dup${i}"
    fi

    mv -- "$path" "$target"
    printf "%s переміщений\n" "$name"

  else
    printf "%s пропущено (не файл і не директорія)\n" "$name"
  fi
done < <(find "$TARGET_DIR" -mindepth 1 -maxdepth 1 -printf '%P\0' | sort -z)