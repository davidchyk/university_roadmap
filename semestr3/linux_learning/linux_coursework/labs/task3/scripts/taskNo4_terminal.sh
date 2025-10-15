#!/usr/bin/env bash
# taskNo4_terminal.sh - відкрити НОВЕ вікно терміналу, запустити taskNo4_main.sh і залишити вікно відкритим
set -euo pipefail

SELF_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
MAIN="$SELF_DIR/taskNo4_main.sh"

# 1) Визначаємо ціль: якщо не задано - беремо поточну директорію В МОМЕНТ ЗАПУСКУ і робимо її абсолютною
RAW_TARGET="${1:-$(pwd -P)}"
# realpath з фолбеком
if ! TARGET="$(realpath -- "$RAW_TARGET" 2>/dev/null)"; then
  TARGET="$RAW_TARGET"
fi

[[ -x "$MAIN" ]] || { echo "Помилка: зроби виконуваним $MAIN (chmod +x taskNo4_main.sh)" >&2; exit 1; }

# Якщо немає GUI - виконаємо в поточному терміналі з паузою
if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
  bash --noprofile --norc "$MAIN" "$TARGET" || true
  read -r -p "Натисни Enter, щоб завершити..." _
  exit 0
fi

# Команда для нового вікна: просто викликаємо main з АБСОЛЮТНОЮ ціллю, потім пауза
inner=$(printf "%q " "$MAIN" "$TARGET")
inner+=$'; echo; echo "Завершено"; read -n1 -s -r -p "Натисни будь-яку клавішу, щоб закрити..."'

if command -v gnome-terminal >/dev/null 2>&1; then
  gnome-terminal -- bash --noprofile --norc -c "$inner"
elif command -v konsole >/dev/null 2>&1; then
  konsole --noclose -e bash --noprofile --norc -c "$inner"
elif command -v xfce4-terminal >/dev/null 2>&1; then
  xfce4-terminal --hold -e bash --noprofile --norc -c "$inner"
elif command -v kitty >/dev/null 2>&1; then
  kitty bash --noprofile --norc -c "$inner"
elif command -v alacritty >/dev/null 2>&1; then
  alacritty -e bash --noprofile --norc -c "$inner"
elif command -v xterm >/dev/null 2>&1; then
  xterm -hold -e bash --noprofile --norc -c "$inner"
else
  echo "Не знайдено відомого GUI-термінала. Встанови, напр.: sudo pacman -S xterm" >&2
  exit 1
fi