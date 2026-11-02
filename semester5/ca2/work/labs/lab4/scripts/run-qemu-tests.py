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


def main():
    parser = argparse.ArgumentParser(description="Run Lab 4 module tests in QEMU")
    parser.add_argument("--kernel", required=True, type=Path)
    parser.add_argument("--initrd", required=True, type=Path)
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    command = [
        "qemu-system-arm",
        "-machine", "virt",
        "-m", "512",
        "-nographic",
        "-kernel", str(args.kernel),
        "-initrd", str(args.initrd),
        "-append", "root=/dev/ram0 rw console=ttyAMA0,115200 mem=512M",
    ]
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    output = bytearray()

    tests = """\
echo '=== LAB 4: KERNEL MODULE TESTS ==='
uname -a
ls -l /root/hello.ko

echo '=== TEST 1: DEFAULT count=1 ==='
dmesg -c >/dev/null
insmod /root/hello.ko
cat /sys/module/hello/parameters/count
rmmod hello
dmesg

echo '=== TEST 2: count=0 ==='
dmesg -c >/dev/null
insmod /root/hello.ko count=0
cat /sys/module/hello/parameters/count
rmmod hello
dmesg

echo '=== TEST 3: count=3 ==='
dmesg -c >/dev/null
insmod /root/hello.ko count=3
cat /sys/module/hello/parameters/count
rmmod hello
dmesg

echo '=== TEST 4: count=7 ==='
dmesg -c >/dev/null
insmod /root/hello.ko count=7
cat /sys/module/hello/parameters/count
rmmod hello
dmesg

echo '=== TEST 5: count=11 (EXPECTED FAILURE) ==='
dmesg -c >/dev/null
insmod /root/hello.ko count=11
echo "insmod exit status: $?"
lsmod | grep '^hello ' || echo 'hello is not loaded'
dmesg

echo '=== TESTS COMPLETE ==='
poweroff
"""

    try:
        wait_for(selector, process, output, b"Please press Enter", args.timeout)
        process.stdin.write(b"\n")
        process.stdin.flush()
        wait_for(selector, process, output, b"/ #", 10)
        process.stdin.write(tests.encode())
        process.stdin.flush()

        deadline = time.monotonic() + args.timeout
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


if __name__ == "__main__":
    main()
