# Roobi Config AnyOS

## Project Goal
The primary aim of this project is to **decouple the lifecycle of the Radxa Rock 5 ITX board from the hosting capabilities of Radxa**. 

By self-hosting the configuration files (`json`), bootloader scripts, and vital support artifacts required by the Roobi installer, this repository ensures that I can continue to reinstall and manage operating systems on my hardware even if the official Radxa servers go offline or older release files are removed.

It serves as a self-contained "Custom Image Source" for the Roobi OS installer.

## How to Use
1.  In the Roobi Installer interface, look for "Advanced Features" or "Settings".
2.  Find the option to add a **Custom Image Source**.
3.  Input the raw URL to the `list.json` file in this repository:
    ```
    https://raw.githubusercontent.com/nyecov/roobi-config-anyOS/main/customList/list.json
    ```
4.  The custom OS entries (like the Armbian OMV build) will now appear in your installation list.

## Attribution
This repository was generated and structured with the assistance of **Antigravity** to accelerate development time.
