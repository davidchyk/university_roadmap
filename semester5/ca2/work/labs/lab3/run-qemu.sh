#!/usr/bin/env bash
set -euo pipefail
lab_dir="${BBB_LAB:-$HOME/bbb-lab}"
busybox_dir="$lab_dir/repos/busybox"
for artifact in "$busybox_dir/_install/boot/zImage" "$busybox_dir/rootfs.cpio.gz"; do
  if [[ ! -r "$artifact" ]]; then
    printf 'Missing file: %s\n' "$artifact" >&2
    exit 1
  fi
done
exec qemu-system-arm \
  -machine virt -m 512 -nographic \
  -kernel "$busybox_dir/_install/boot/zImage" \
  -initrd "$busybox_dir/rootfs.cpio.gz" \
  -append 'root=/dev/ram0 rw console=ttyAMA0,115200 mem=512M'
