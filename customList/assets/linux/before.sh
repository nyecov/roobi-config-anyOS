#! /bin/bash

set -e

current_script_path='.'

_reboot=0

python3 fast_flash_spi.py spi_image.xz /dev/mtdblock0

# ======== u-boot =========

rock_5_itx_file="$current_script_path/u-boot-rock-5-itx_*.deb"

rknext_file="$current_script_path/u-boot-rknext_*.deb"

rknext_version=$(dpkg --info $rknext_file | grep Version | awk '{{print $2}}')

version_file=/usr/Roobi/u-boot-version.txt

if [[ ! -f $version_file  ]] || [[ $(cat $version_file) != $rknext_version ]];then
    dpkg -i $rknext_file $rock_5_itx_file 

    root_device=$(df -P / | awk 'NR==2 {{print $1}}')
    physical_device=$(lsblk -no PKNAME "$root_device")

    systemctl mask reboot.target
    systemctl mask poweroff.target
    systemctl mask halt.target
    
    /usr/lib/u-boot/rock-5-itx/setup.sh update_bootloader /dev/$physical_device || return_value=$?

    if [ $return_value -eq 0 ]; then
        echo $rknext_version > $version_file || true
        
        # Update Boot Order
        if [ -f "$current_script_path/setup_boot_order.sh" ]; then
            chmod +x "$current_script_path/setup_boot_order.sh"
            bash "$current_script_path/setup_boot_order.sh" || echo "Warning: Failed to update boot order"
        fi
    fi
    systemctl unmask reboot.target
    systemctl unmask poweroff.target
    systemctl unmask halt.target
    sync
    echo "Update Bootloader Success!"
else
    echo "Bootloader up to date!"
fi

