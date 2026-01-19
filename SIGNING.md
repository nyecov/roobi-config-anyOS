# Signing Guide

This repository uses signatures to ensure the authenticity and integrity of download assets (like the bootloader scripts). Roobi verifies these signatures before executing any downloaded code.

## 1. Why is this required?

When you fork this repository or add your own custom assets (like `setup_boot_order.sh`), the original signatures (signed by the original author) become invalid for your modified files. 

Since you do not have the original private key, you must **Re-sign all assets** with your own key and configure Roobi to trust it.

## 2. Automated Signing (Recommended)

This repository includes a tool to automate the process.

### Step 1: Generate Keypair & Sign
Run the update tool:
```bash
./tools/update_signatures.py
```
- If `private.pem` is missing, it will generate a new RSA-2048 keypair for you.
- It will scan all JSON files and re-calculate the MD5, Size, and Signature for every asset.
- It will verify that `private.pem` is added to `.gitignore`.
- **Output**: It will display your **Public Key** at the end.

### Step 2: Configure Roobi

To make your Roobi device trust your new signatures, you must add your **Public Key** to the device.

1.  **SSH into your Roobi device**.
2.  **Locate the existing public key**. Roobi typically stores this in the application directory or system configuration.
    - Try running: `find /opt /etc /usr -name "*.pem"` or look for `public_key` in the settings.
3.  **Replace or Add your Key**.
    - Overwrite the existing `public.pem` (or equivalent) with the content of your new key (displayed by the `update_signatures.py` tool).
    - If there is a configuration file listing trusted keys, add yours to the list.
4.  **Restart Roobi** to apply changes.

## 3. Manual Signing

If you prefer to sign files manually (e.g., for a specific single file):

**Format**: RSA-2048 (SHA256), Base64 encoded.

```bash
# 1. Generate Signature
openssl dgst -sha256 -sign private.pem -out signature.bin path/to/file

# 2. Encode to Base64 (copy this output to JSON "sig" field)
base64 -w 0 signature.bin
```

## 4. Key Security

*   **`private.pem`**: NEVER commit this file. Keep it safe on your local machine.
*   **`public.pem`**: This can be shared or committed if necessary, but Roobi needs the content of this key.
