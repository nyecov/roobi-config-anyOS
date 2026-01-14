# Roobi Custom Image Source Design Guide

## UUID Format

The `uuid` field in `list.json` and the corresponding OS configuration JSON files uses a specific format:

*   **Format**: Standard UUID (Universally Unique Identifier) **without hyphens**.
*   **Length**: 32 hexadecimal characters.
*   **Example**: 
    *   Standard UUID: `26cbf15b-3066-431d-8641-8809b7468fae`
    *   Roobi UUID: `26cbf15b3066431d86418809b7468fae`

To generate a valid UUID, you can generate a standard UUIDv4 and remove all `-` characters.

## OS Configuration JSON Elements

The OS specific JSON file (e.g., `omv_bookworm.json`) instructs Roobi on how to download and install the operating system. Below are the key elements based on `Armbian_24.8.2_Rock-5-itx_bookworm_vendor_6.1.75_minimal.json`.

### Root Object

| Key | Type | Description |
| :--- | :--- | :--- |
| `script_version` | String | Version of the script format. Currently fixed at `"1"`. |
| `uuid` | String | Unique identifier. **Must match** the UUID defined in the master `list.json`. |
| `name` | String | Display name of the OS (e.g., "Armbian Bookworm CLI"). |
| `version` | String | Version string of the OS build (e.g., "24.8.2"). |
| `author` | String | Name of the maintainer or organization (e.g., "Armbian"). |
| `date` | String | Release date, typically in `YYYY-MM-DD` or `YYYY.MM.DD` format. |
| `img` | String | URL to a logo or icon image (SVG or PNG) representing the OS. |
| `description` | Object | Localized descriptions. Keys are language codes (e.g., `"en"`, `"zh-CN"`). |
| `download` | Array | A list of file objects to be downloaded. |
| `scripts` | Array | Installation execution logic. |

### Download Object (`download`)

Each item in the `download` array represents a file resource required for installation. This typically includes the main OS image and optional hook scripts or flash tools.

| Key | Type | Description |
| :--- | :--- | :--- |
| `file_name` | String | The local filename to save the download as (e.g., `install.img.xz`, `before.sh`). |
| `size` | Number | File size in bytes. |
| `urls` | Array | A list of URL strings (mirrors) to download the file from. |
| `md5` | String | MD5 checksum of the file for integrity verification. |
| `sig` | String | (Optional) Cryptographic signature for authenticity. |

### File Verification Fields
The `download` object relies on specific fields to ensure the file downloaded correctly and is authentic:

*   **`size`**: The size of the file in bytes.
    *   **Purpose**: Roobi uses this to verify the download completeness and calculate progress chunks.
    *   **Value**: Integer (e.g., `1027208`).

*   **`md5`**: The MD5 checksum of the file.
    *   **Purpose**: Ensures **Integrity**. Roobi calculates the MD5 of the downloaded file and compares it to this string to ensure the file was not corrupted during download.
    *   **Value**: 32-character hexadecimal string.

*   **`sig`**: A cryptographic signature.
    *   **Purpose**: Ensures **Authenticity**. It allows Roobi to verify that the file was signed by a trusted entity (Radxa/Palmshell) and hasn't been tampered with by a man-in-the-middle.
    *   **Value**: Base64 encoded signature string.

### Common Downloadable Resources

Beyond the main OS image, you can include other resources in the `download` array. Based on the reference Armbian configuration, here are categorized examples:

#### 1. Lifecycle Scripts (`before.sh` / `after.sh`)
Scripts that execute at specific stages of the installation process.
*   **Example**: `before.sh`
*   **Purpose**: Actions to perform before the main image is written to disk (e.g., clearing signatures, verifying hardware).

#### 2. Installation Tools (`*.py`, `*.sh`)
Helper scripts or binaries used by the lifecycle scripts to perform complex tasks.
*   **Example**: `fast_flash_spi.py`
*   **Purpose**: A Python script used to flash the SPI memory, likely invoked by `before.sh` or `after.sh`.

#### 3. Firmware Images (`spi_image.*`)
Binary images for specific hardware components, separate from the main OS disk.
*   **Example**: `spi_image.xz`
*   **Purpose**: The actual bootloader binary to be flashed to the board's SPI flash memory.

#### 4. System Packages (`*.deb`, `*.rpm`)
Package files that might be installed into the target system or used to provide binaries for the installation process.
*   **Example**: `u-boot-rknext_..._arm64.deb`
*   **Purpose**: Debian packages containing U-Boot bootloader files.

### Scripts Object (`scripts`)

Defines the installation procedure.

| Key | Type | Description |
| :--- | :--- | :--- |
| `type` | String | usually `"auto"`. Tells Roobi to handle image writing automatically. |
| `text` | String | Command text, usually `"start"`. |
| `size` | Number | **Install Size (Uncompressed)**. The exact size of the OS on disk after installation (bytes). This is used for checking disk capacity and calculating the progress bar. |

## Repository Structure & Custom Assets

To create a robust custom OS source that persists even if official servers disappear, this repository adopts a self-contained structure:

1.  **`customList/list.json`**: The entry point.
    *   This is the URL you give to Roobi custom source settings.
    *   It acts as a catalog pointing to individual OS JSON files.

2.  **`customList/assets/`**: The "Warehouse".
    *   Contains the **Critical Support Files** needed for installation:
        *   `before.sh`: Pre-install logic (e.g., flashing SPI ROM).
        *   `fast_flash_spi.py`: Tool to write firmware.
        *   `spi_image.xz`: The actual bootloader firmware binary.
        *   `*.deb`: U-Boot packages required to update the board state.
        *   `pic/*.svg`: OS logos/icons.
    *   By hosting these here, we ensure the "logic" of the install is safe.

3.  **`customList/os_configs/*.json`**: The "Blueprints".
    *   (e.g., `Armbian_...omv_minimal.json`)
    *   These files define *how* to combine the **assets** (from this repo) and the **Main OS Image** (usually from an external mirror like `dl.armbian.com`) to perform a complete installation.

### Why include supporting files?
Simple OS installs just write an image to a disk. Complex installs (like for the Rock 5 ITX) often require updating the board's internal firmware (SPI Flash) to match the incoming OS. By bundling these scripts and binaries in the `assets` folder and referencing them in the `download` array of your JSON, you ensure the installation succeeds even on a board with outdated firmware.

### Shared Utilities (Linux)
Across different Linux distributions for the same hardware (e.g., Rock 5 ITX), the "utility" files required for the bootloader update process are often identical.
*   **Observation**: Whether you are installing Ubuntu 24.04, Armbian Noble, or Debian Bookworm on the Rock 5 ITX (`ps009`), they all utilize the exact same `before.sh`, `fast_flash_spi.py`, `spi_image.xz`, and **U-Boot Debian packages** (`u-boot-rknext...` and `u-boot-rock-5-itx...`).
*   **Benefit**: This means you can reuse the same assets in your `customList/assets/` folder for multiple different Linux OS entries for the same board.
*   **Note**: This pattern applies primarily to Linux-based images sharing the same boot rom requirements. **Windows 10** installations, for example, do **not** use `before.sh` or the SPI flash tools; instead, they utilize an `after.sh` script and rely on a pre-existing UEFI environment. Always reference an existing working JSON for your specific OS family.
