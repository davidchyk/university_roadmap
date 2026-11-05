#!/usr/bin/env bash
set -euo pipefail

bbb_lab="${BBB_LAB:-$HOME/bbb-lab}"
kernel_dir="${KDIR:-$bbb_lab/repos/linux-stable}"
toolchain_bin="$bbb_lab/toolchains/gcc-arm-8.3-2019.03-x86_64-arm-eabi/bin"
lab_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$lab_dir/src"

export ARCH=arm
export CROSS_COMPILE="ccache arm-eabi-"
export KDIR="$kernel_dir"
export PATH="$toolchain_bin:$PATH"
export CCACHE_DIR="${CCACHE_DIR:-$lab_dir/build/ccache}"

mkdir -p "$CCACHE_DIR" "$lab_dir/evidence"

for source in "$source_dir/hello1.c" "$source_dir/hello2.c" \
	"$source_dir/inc/hello1.h"; do
	"$KDIR/scripts/checkpatch.pl" --no-tree -f "$source"
done

make -C "$source_dir" clean
make -C "$source_dir" -j"$(nproc)"
file "$source_dir/hello1.ko" "$source_dir/hello2.ko"
modinfo "$source_dir/hello1.ko"
modinfo "$source_dir/hello2.ko"
