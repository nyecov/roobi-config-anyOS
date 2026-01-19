# Changing Boot Device Order on Rock 5 ITX

It is possible to change the device boot order (e.g., prioritize NVMe over SD card, or USB over everything) **without reflashing the bootloader**.

The Rock 5 ITX uses the U-Boot bootloader stored on the SPI Flash (`/dev/mtd0`). The boot sequence is controlled by a U-Boot environment variable called `boot_targets`.

## Prerequisite
- **Serial Console**: You need a USB-to-TTL adapter connected to the debug UART pins.
- **OR Keyboard & Monitor**: If your U-Boot version supports video output (EDP/HDMI) and USB keyboard during boot (most modern builds do).

## Procedure (U-Boot Console)

This is the safest method as it interacts directly with the bootloader.

1.  **Reboot the board**.
2.  **Interrupt Boot**: As soon as you see the boot logs (or the logo), press `Ctrl+C` or `Space` repeatedly to stop the autoboot process. You should see a prompt like `=>` or `rock5b #`.
3.  **Check Current Order**:
    Run the following command to see the current order:
    ```bash
    printenv boot_targets
    ```
    *Example output:* `boot_targets=usb0 mmc1 nvme0 nvme1 scsi0 mmc0 pxe dhcp`
    
    *Legend:*
    *   `mmc1`: MicroSD Card
    *   `mmc0`: eMMC (On-board)
    *   `nvme0`: M.2 NVMe SSD
    *   `usb0`: USB Storage
    *   `scsi0`: SATA

4.  **Set New Order**:
    Define your desired order. For example, to boot from **NVMe** first, then **SD Card**, then **USB**:
    ```bash
    setenv boot_targets "nvme0 mmc1 usb0 mmc0"
    ```

5.  **Save Changes**:
    Write the changes to the SPI flash environment sector:
    ```bash
    saveenv
    ```
    *Output should confirm:* `Saving Environment to SPI Flash... OK`

6.  **Boot**:
    Resume the boot process:
    ```bash
    boot
    ```

## Method 3: Automated Script (During OS Install)

This repository now includes a script `setup_boot_order.sh` that is called by the OS installer (`before.sh`).
It attempts to set the boot order to `scsi0 nvme0 mmc1 usb0` automatically (Prioritizing SATA).
- Requires `u-boot-tools`.
- Uses a default environment offset `0x7C0000` (common for Rockchip SPI).
- Located in `customList/assets/linux/`.

> **Important**: This script must be **signed**. 
> If you modify it, you must re-generate the signature. See **[Signing Guide](SIGNING.md)** for instructions.

## How to Revert
To revert the boot order to the factory default, simply **Reinstall the OS** using the standard "Armbian Linux OpenMediaVault included" option (the one *without* "(SATA Boot)" in the name).
This works because the installation process completely rewrites the 16MB SPI Flash, wiping your custom environment settings.

## Notes
- This change persists across reboots.
- This change survives OS reinstallations (as they don't touch the SPI flash).
- If you reflash the SPI bootloader (e.g., using `rkdeveloptool` or `fast_flash_spi.py` from this repo), the environment **will be reset** to defaults.
