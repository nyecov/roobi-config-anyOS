#!/bin/bash
set -e

# Configuration for Rock 5 ITX SPI Flash Environment
# Assuming environment is at 0x7C0000 (just before 8MB Mark)
# If this is incorrect for your specific U-Boot build, update the offset.
ENV_DEV="/dev/mtd0"
ENV_OFFSET="0x7C0000"
ENV_SIZE="0x8000" # 32KB
ENV_SECT_SIZE="0x1000" # 4KB

CONFIG_FILE="/etc/fw_env.config"

# Ensure u-boot-tools is available
if ! command -v fw_setenv &> /dev/null; then
    echo "fw_setenv not found. Installing u-boot-tools..."
    if command -v apt-get &> /dev/null; then
        apt-get update && apt-get install -y u-boot-tools || echo "Failed to install u-boot-tools"
    fi
fi

if ! command -v fw_setenv &> /dev/null; then
    echo "Error: fw_setenv tool missing. Cannot update boot order."
    exit 1
fi

# Create config if missing
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Generating $CONFIG_FILE..."
    echo "$ENV_DEV $ENV_OFFSET $ENV_SIZE $ENV_SECT_SIZE" > "$CONFIG_FILE"
fi

# Set Boot Order: SATA -> NVMe -> SD -> USB
# Adjust this string to your preference
NEW_ORDER="scsi0 nvme0 mmc1 usb0"

echo "Setting boot_targets to: $NEW_ORDER"
fw_setenv boot_targets "$NEW_ORDER"

echo "Boot order updated successfully."
