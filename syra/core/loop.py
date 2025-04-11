from syra.config import load_config
from syra.core.speech.speech import speech_loop

config = load_config()
max_cycles = 5  # safety limit for now

def main_loop():
    print("[LOOP] Starting SYRA main loop...")
    cycles = 0
    while True:
        speech_loop()
        cycles += 1
        if cycles >= max_cycles:
            print("[LOOP] Max cycles reached, exiting.")
            break

if __name__ == "__main__":
    main_loop()