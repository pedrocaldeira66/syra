from syra.config import load_config
from syra.core.speech.stt_engines import get_stt_engine
from syra.core.speech.tts_engines import get_tts_engine
from syra.core.reasoning.reasoning import analyze
from syra.core.memory.memory import save_interaction
import time

config = load_config()
stt = get_stt_engine(config)
tts = get_tts_engine(config)

def speech_loop():
    print("[SPEECH] SYRA is listening...")
    try:
        while True:
            user_input = stt.listen()

            if not user_input or not user_input.strip():
                print("[SPEECH] No input detected. Listening again...")
                time.sleep(1)
                continue

            print(f"[SPEECH] Heard: {user_input}")
            response = analyze(user_input)

            if response:
                print(f"[SPEECH] Responding: {response}")
                tts.speak(response)
                save_interaction(user_input, response)
            else:
                print("[SPEECH] No response generated.")

            # Add delay to simulate natural pacing
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n[SPEECH] User interrupted the loop.")
    except Exception as e:
        print(f"[SPEECH ERROR] {e}")