#!/usr/bin/python3

import os
import sys

BLOCK_SIZE = 4096


def process(spi_file, device):
    with open(device, 'rb') as f:
        blk_data = f.read()

    with open(spi_file, 'rb') as f:
        spi_data = f.read()

    now = 0

    device_fd = os.open(device, os.O_WRONLY, )
    f = os.fdopen(device_fd, 'wb', 0)

    while now + BLOCK_SIZE < len(spi_data):
        if blk_data[now:now + BLOCK_SIZE] != spi_data[now:now + BLOCK_SIZE]:
            f.seek(now)
            f.write(spi_data[now:now + BLOCK_SIZE])
        now += BLOCK_SIZE
    f.close()


if __name__ == "__main__":
    try:
        spi_file = sys.argv[1]
        device = sys.argv[2]
    except IndexError:
        print("USAGE: python3 fast_flash_spi.py <spi_file> <spi_device>")
        exit(1)
    print("Writing SPI Flash, Please wait...", flush=True)
    process(spi_file, device)
