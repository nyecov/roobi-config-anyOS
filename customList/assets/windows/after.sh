echo -e "w" | fdisk {disk}

sleep 0.1

echo -e "resizepart 2 100% \n quit" | parted {disk} > /dev/null

if echo "{disk}" | grep -q "nvme";then
    echo y |ntfsresize {disk}p2 > /dev/null
else
    echo y |ntfsresize {disk}2 > /dev/null
fi