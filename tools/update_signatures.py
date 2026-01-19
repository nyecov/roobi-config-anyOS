#!/usr/bin/env python3
import json
import os
import hashlib
import base64
import glob
import subprocess
import sys

# Requirements: openssl installed in system
DATA_DIR = "customList"
ASSETS_DIR = "customList/assets"
KEY_FILE = "private.pem"
PUB_FILE = "public.pem"

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True)

def generate_keys():
    print(f"Generating new RSA-2048 keypair: {KEY_FILE}")
    run_cmd(f"openssl genrsa -out {KEY_FILE} 2048")
    run_cmd(f"openssl rsa -in {KEY_FILE} -pubout -out {PUB_FILE}")
    print(f"Public key saved to {PUB_FILE}. Configuring Roobi to use this key is required.")

def sign_file(filepath, keypath):
    # openssl dgst -sha256 -sign private.pem -out signature.bin file
    sig_bin = "temp_sig.bin"
    try:
        cmd = f"openssl dgst -sha256 -sign {keypath} -out {sig_bin} {filepath}"
        run_cmd(cmd)
        with open(sig_bin, "rb") as f:
            sig_data = f.read()
        return base64.b64encode(sig_data).decode('utf-8')
    finally:
        if os.path.exists(sig_bin):
            os.remove(sig_bin)

def calculate_md5(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_asset(filename):
    # Search recursively in assets dir
    for root, dirs, files in os.walk(ASSETS_DIR):
        if filename in files:
            return os.path.join(root, filename)
    return None

def process_json(json_path):
    print(f"Processing {json_path}...")
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    changed = False
    
    if "download" in data:
        for item in data["download"]:
            fname = item.get("file_name")
            if not fname:
                continue
            
            # Find the file locally
            local_path = find_asset(fname)
            if not local_path:
                print(f"  [WARN] File not found locally: {fname}. Skipping.")
                continue
            
            # Calculate Size
            size = os.path.getsize(local_path)
            item["size"] = size
            
            # Calculate MD5
            md5 = calculate_md5(local_path)
            item["md5"] = md5
            
            # Sign
            sig = sign_file(local_path, KEY_FILE)
            item["sig"] = sig
            
            print(f"  [OK] Signed {fname} (Size: {size})")
            changed = True
            
    if changed:
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)
        print("  Updated JSON.")

def main():
    if not os.path.exists(KEY_FILE):
        print(f"Private key {KEY_FILE} not found.")
        reply = input("Do you want to generate a new keypair? (y/n): ")
        if reply.lower() == 'y':
            generate_keys()
        else:
            print("Aborted. Please provide private.pem to sign files.")
            sys.exit(1)
            
    # Process all JSONs in customList root
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    # Exclude list.json usually, but it doesn't have 'download' so it's safe
    
    for jf in json_files:
        if "list.json" in jf:
            continue
        process_json(jf)
        
    print("\nAll Done.")
    if os.path.exists(PUB_FILE):
        print(f"\nYour Public Key ({PUB_FILE}):")
        with open(PUB_FILE, 'r') as f:
            print(f.read())
        print("Copy this public key to your Roobi configuration.")

if __name__ == "__main__":
    main()
