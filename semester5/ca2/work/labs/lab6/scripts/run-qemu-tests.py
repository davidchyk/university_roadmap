#!/usr/bin/env python3

import argparse
import selectors
import subprocess
import sys
import time
from pathlib import Path


def read_available(selector, process, output):
    for key, _ in selector.select(timeout=0.25):
        chunk = key.fileobj.read1(65536)
        if chunk:
            output.extend(chunk)
            sys.stdout.buffer.write(chunk)
            sys.stdout.buffer.flush()


def wait_for(selector, process, output, marker, timeout):
    deadline = time.monotonic() + timeout
    while marker not in output:
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Timed out waiting for {marker!r}")
        read_available(selector, process, output)
        if process.poll() is not None:
            raise RuntimeError(f"QEMU exited with status {process.returncode}")


def run_qemu(kernel, initrd, commands, timeout):
    command = [
        "qemu-system-arm", "-machine", "virt", "-m", "512", "-nographic",
        "-kernel", str(kernel), "-initrd", str(initrd),
        "-append", "root=/dev/ram0 rw console=ttyAMA0,115200 mem=512M",
    ]
    process = subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    output = bytearray()

    try:
        wait_for(selector, process, output, b"Please press Enter", timeout)
        process.stdin.write(b"\n")
        process.stdin.flush()
        wait_for(selector, process, output, b"/ #", 10)
        process.stdin.write(commands.encode())
        process.stdin.flush()

        deadline = time.monotonic() + timeout
        while process.poll() is None:
            if time.monotonic() >= deadline:
                raise TimeoutError("Timed out waiting for QEMU to power off")
            read_available(selector, process, output)
        read_available(selector, process, output)
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=5)

    if process.returncode != 0:
        raise RuntimeError(f"QEMU exited with status {process.returncode}")
    return bytes(output)


def main():
    parser = argparse.ArgumentParser(description="Run Lab 6 debugging tests")
    parser.add_argument("--kernel", required=True, type=Path)
    parser.add_argument("--initrd", required=True, type=Path)
    parser.add_argument("--timeout", type=int, default=90)
    args = parser.parse_args()

    allocation_commands = """\
echo '=== LAB 6 TEST 1: FORCED KMALLOC FAILURE ==='
uname -a
dmesg -c >/dev/null
insmod /root/hello.ko count=5
echo "insmod exit status: $?"
lsmod | grep '^hello ' || echo 'hello is not loaded'
dmesg
echo '=== ALLOCATION TEST COMPLETE ==='
poweroff
"""

    bug_commands = """\
echo '=== LAB 6 TEST 2: BUG_ON count=11 ==='
dmesg -c >/dev/null
insmod /root/hello.ko count=11
echo "insmod exit status: $?"
lsmod
echo 'module section addresses:'
for section in .text .init.text .data; do
    printf '%s: ' "$section"
    cat "/sys/module/hello/sections/$section" 2>/dev/null || echo unavailable
done
rmmod hello
echo "rmmod exit status: $?"
dmesg
echo '=== BUG TEST COMPLETE ==='
poweroff
"""

    print("\n=== QEMU SESSION A ===", flush=True)
    run_qemu(args.kernel, args.initrd, allocation_commands, args.timeout)
    print("\n=== QEMU SESSION B ===", flush=True)
    run_qemu(args.kernel, args.initrd, bug_commands, args.timeout)


if __name__ == "__main__":
    main()
