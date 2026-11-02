#!/usr/bin/env bash
set -euo pipefail

bbb_lab="${BBB_LAB:-$HOME/bbb-lab}"
kernel_dir="${KDIR:-$bbb_lab/repos/linux-stable}"
toolchain_bin="$bbb_lab/toolchains/gcc-arm-8.3-2019.03-x86_64-arm-eabi/bin"
source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"

export ARCH=arm
export CROSS_COMPILE="ccache arm-eabi-"
export KDIR="$kernel_dir"
export PATH="$toolchain_bin:$PATH"
export CCACHE_DIR="${CCACHE_DIR:-$source_dir/../build/ccache}"

mkdir -p "$CCACHE_DIR"

"$KDIR/scripts/checkpatch.pl" --no-tree -f "$source_dir/hello.c"
make -C "$source_dir" clean
make -C "$source_dir" -j"$(nproc)"
file "$source_dir/hello.ko"
modinfo "$source_dir/hello.ko"
