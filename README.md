# AnyRoobi

## Project Goal
The resource to provide a platform to add **any OS** to a custom list, simplifying the process of expanding the operating system choices for Roobi-compatible devices.

While initially created to decouple the lifecycle of the Radxa Rock 5 ITX board from official repositories, this project serves as a template and toolset for anyone wishing to curate their own OS catalogs.

It serves as a self-contained "Custom Image Source" for the Roobi OS installer.

## Memento & Hardware Context
**This repository exists as a "Time Capsule" for myself.**

I own a **Radxa Rock 5 ITX (16GB RAM) v1.11 model**. The primary purpose of this project is to ensure that years from now—when links have rotted, wikis have moved, and my memory has faded—I can still perform a clean, working installation of my preferred OS on this specific hardware. All necessary scripts, bootloaders, and logic are archived here to withstand the test of time.

> **Disclaimer**: While I have forked key repositories (like [Docs](https://github.com/nyecov/radxa-docs-fork) and [BSP](https://github.com/nyecov/radxa-bsp)) to safeguard them, **always use the [Official Radxa Repositories](https://github.com/radxa-docs) and [Wiki](https://radxa.com/products/rock5/5itx/#documentation) for the most up-to-date information.** My forks are static snapshots and are not promised to stay in sync.

## How to Use
1.  In the Roobi Installer interface, look for "Advanced Features" or "Settings".
2.  Find the option to add a **Custom Image Source**.
3.  Input the raw URL to the `list.json` file in this repository:
    ```
    https://raw.githubusercontent.com/nyecov/roobi-config-anyOS/main/customList/list.json
    ```
4.  The custom OS entries will now appear in your installation list.
    > **Target OS Details**: This configuration installs **Armbian Linux OpenMediaVault included**.
    > *   **Source URL**: [https://dl.armbian.com/rock-5-itx/Bookworm_vendor_minimal-omv](https://dl.armbian.com/rock-5-itx/Bookworm_vendor_minimal-omv)
    > *   **Found On**: [https://www.armbian.com/radxa-rock-5-itx/](https://www.armbian.com/radxa-rock-5-itx/)
    >
    > *Note: A second entry ("Armbian OMV Time Capsule") is also included, which pulls from a static GitHub Release backup in case the official servers are down.*

## Documentation
For detailed guides on how this repository works, how to build custom assets, and troubleshooting, please visit the **[Project Wiki](https://github.com/nyecov/roobi-config-anyOS/wiki)**.
    

## Attribution
This repository was generated and structured with the assistance of **Antigravity** to accelerate development time.
