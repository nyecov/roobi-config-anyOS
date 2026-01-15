# btusb.ko (Kernel Module)

## What is this file?
`btusb.ko` is a compiled Linux kernel module ("ko" stands for Kernel Object). It is the driver for **Bluetooth USB dongles/controllers**.

## Why is it included here?
The `ps006` (Palmshell Pocket?) appears to use a Bluetooth chip that is either:
1.  Not supported by the standard Linux kernel version shipped with the Ubuntu 22.04 image.
2.  Requires a specific patched version to function correctly on this specific hardware.

## How is it used?
It is used in conjunction with `after.sh`.
1.  Roobi downloads this file.
2.  Roobi executes `after.sh`.
3.  `after.sh` manually copies this file from the download cache into the target system's module directory:
    `/lib/modules/6.2.0-26-generic/kernel/drivers/bluetooth/`
    
This approach effectively "hotfixes" the OS image immediately after installation, without needing to repack the entire OS image just to update one driver.
