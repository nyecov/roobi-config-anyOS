# RoobiVault

## Project Goal
The resource to provide a platform to add **any OS** to a custom list, simplifying the process of expanding the operating system choices for Roobi-compatible devices.

While initially created to decouple the lifecycle of the Radxa Rock 5 ITX board from official repositories, this project serves as a template and toolset for anyone wishing to curate their own OS catalogs.

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
