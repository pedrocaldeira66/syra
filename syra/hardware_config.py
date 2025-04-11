import json
import os

def load_hardware_config(path="./.hardware_config"):
    full_path = os.path.abspath(path)
    if not os.path.exists(full_path):
        print(f"[WARN] .hardware_config file not found at: {full_path}")
        return {}

    print(f"[CONFIG] Loaded hardware config from: {full_path}")
    with open(full_path, "r") as f:
        return json.load(f)
