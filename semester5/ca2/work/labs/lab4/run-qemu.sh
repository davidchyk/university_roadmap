#!/usr/bin/env bash
set -euo pipefail

kernel="${KERNEL:-$HOME/bbb-lab/repos/busybox/_install/boot/zImage}"
initrd="${INITRD:-${1:-$HOME/bbb-lab/repos/busybox/rootfs.cpio.gz}}"

command -v qemu-system-arm >/dev/null || {
	printf 'Помилка: qemu-system-arm не встановлено.\n' >&2
	exit 1
}

for image in "$kernel" "$initrd"; do
	if [[ ! -f "$image" ]]; then
		printf 'Помилка: файл не знайдено: %s\n' "$image" >&2
		exit 1
	fi
done

exec qemu-system-arm \
	-machine virt \
	-m 512 \
	-nographic \
	-kernel "$kernel" \
	-initrd "$initrd" \
	-append 'root=/dev/ram0 rw console=ttyAMA0,115200 mem=512M'
