from core.reasoning import reasoning
from syra.config import load_config
from syra.core import hardware, vision, speech, memory
from syra.utils.safe_init import safe_init
from syra.hardware_config import load_hardware_config

def boot_sequence():
    print("[BOOT] Loading SYRA configuration...")
    config = load_config()
    hardware_conf = load_hardware_config()
    config.update(hardware_conf)
    
    print("[BOOT] Initializing hardware interfaces...")
    safe_init(lambda: hardware.initialize(config), name="Hardware")

    print("[BOOT] Initializing vision system...")
    safe_init(lambda: vision.initialize(config), name="Vision")

    print("[BOOT] Initializing speech system...")
    safe_init(lambda: speech.initialize(config), name="Speech")

    print("[BOOT] Initializing reasoning engine...")
    safe_init(lambda: reasoning.initialize(config), name="Reasoning")

    print("[BOOT] Initializing memory system...")
    safe_init(lambda: memory.initialize(config), name="Memory")

    print("[BOOT] SYRA boot sequence complete.")
    return config
