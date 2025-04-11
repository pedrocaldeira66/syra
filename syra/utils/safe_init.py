import importlib
import traceback

def safe_import(module_name, fallback=None, warn=True):
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        if warn:
            print(f"[WARN] Could not import {module_name}: {e}")
        return fallback

def safe_init(init_func, fallback_func=None, name="UnknownModule"):
    try:
        return init_func()
    except Exception as e:
        print(f"[ERROR] {name} failed to initialize: {e}")
        traceback.print_exc()
        if fallback_func:
            print(f"[INFO] Falling back to alternative for {name}")
            return fallback_func()
        return None
