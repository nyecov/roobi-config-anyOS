echo -e "d\n3\nw" | fdisk {disk}

echo -e "resizepart 2 100% \n quit" | parted {disk} > /dev/null

if echo "{disk}" | grep -q "nvme";then
    e2fsck -f {disk}p2
    resize2fs {disk}p2
else
    e2fsck -f {disk}2
    resize2fs {disk}2
fi