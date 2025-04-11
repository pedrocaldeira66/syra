from syra.config import load_config
from syra.core.speech.stt_engines import get_stt_engine
from syra.core.speech.tts_engines import get_tts_engine
from syra.core.reasoning.reasoning import analyze
from syra.core.memory.knowledge_store import update_fact
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

            # Special pattern: teaching SYRA a fact
            if user_input.lower().startswith("remember that"):
                try:
                    _, statement = user_input.split("that", 1)
                    topic, value = statement.strip().split("is", 1)
                    update_fact(topic.strip(), value.strip())
                    response = f"Okay, I'll remember that {topic.strip()} is {value.strip()}."
                except Exception as e:
                    response = "I heard you wanted me to remember something, but I couldn't understand the format."
            else:
                response = analyze(user_input)

            print(f"[SPEECH] Responding: {response}")
            tts.speak(response)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n[SPEECH] Loop interrupted by user.")
    except Exception as e:
        print(f"[SPEECH ERROR] {e}")