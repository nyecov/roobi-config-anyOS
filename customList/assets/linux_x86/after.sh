#!/bin/bash

sync

temp=$(mktemp -d)

partprobe

if echo "{disk}" | grep -q "nvme";then
    mount {disk}p2 "$temp"
else
    mount {disk}2 "$temp"
fi

cp /opt/reming/scripts/58373afacba743b1aa06b8b88dd39211/btusb.ko $temp/lib/modules/6.2.0-26-generic/kernel/drivers/bluetooth/