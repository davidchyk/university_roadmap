#!/usr/bin/env bash
set -euo pipefail

bbb_lab="${BBB_LAB:-$HOME/bbb-lab}"
lab_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_archive="$bbb_lab/repos/busybox/rootfs.cpio.gz"
build_dir="$lab_dir/build/initramfs"
rootfs_dir="$build_dir/rootfs"
output_archive="$build_dir/rootfs-lab5.cpio.gz"

for artifact in "$source_archive" "$lab_dir/src/hello1.ko" \
	"$lab_dir/src/hello2.ko"; do
	if [[ ! -r "$artifact" ]]; then
		printf 'Missing required file: %s\n' "$artifact" >&2
		exit 1
	fi
done

mkdir -p "$rootfs_dir"
find "$rootfs_dir" -mindepth 1 -delete

(
	cd "$rootfs_dir"
	gzip -dc "$source_archive" | cpio -idmu --quiet
	mkdir -p root
	cp "$lab_dir/src/hello1.ko" "$lab_dir/src/hello2.ko" root/
	find . -print0 | cpio --null -o --format=newc --owner=0:0 2>/dev/null \
		| gzip > "$output_archive"
)

gzip -t "$output_archive"
printf '%s\n' "$output_archive"
