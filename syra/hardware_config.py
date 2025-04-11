# syra/hardware_config.py

import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".hardware_config")

def load_hardware_config():
    if not os.path.exists(CONFIG_PATH):
        print("[WARN] .hardware_config file not found. Using defaults.")
        return {}

    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            print(f"[CONFIG] Loaded hardware config from: {CONFIG_PATH}")
            return config
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in .hardware_config: {e}")
        return {}

def get_hardware_component(name, default=None):
    config = load_hardware_config()
    return config.get(name, default)