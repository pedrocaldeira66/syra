from syra.config import load_config
from syra.core.speech.speech import speech_loop

config = load_config()
use_loop = config.get("syra", {}).get("run_loop", True)
max_cycles = config.get("syra", {}).get("max_cycles", 0)  # 0 = unlimited

def main_loop():
    print("[LOOP] Starting SYRA main loop...")
    cycles = 0
    try:
        while True:
            speech_loop()
            cycles += 1
            if max_cycles and cycles >= max_cycles:
                print("[LOOP] Max cycles reached, exiting.")
                break
    except KeyboardInterrupt:
        print("\n[LOOP] Interrupted by user. Exiting gracefully.")

if __name__ == "__main__":
    main_loop()