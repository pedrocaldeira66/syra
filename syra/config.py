import os
import json
from dotenv import load_dotenv

load_dotenv()

def load_env_config():
    return {
        "env": os.getenv("SYRA_ENV", "development"),
        "use_mock": os.getenv("USE_MOCK", "false").lower() == "true",
        "speech": {
            "mode": os.getenv("SPEECH_MODE", "offline"),
            "stt": os.getenv("STT_ENGINE", "mock"),
            "tts": os.getenv("TTS_ENGINE", "mock"),
            "language": os.getenv("LANGUAGE", "en"),
            "vosk_model_path": os.getenv("VOSK_MODEL_PATH", "models/vosk"),
            "online_tts": os.getenv("ONLINE_TTS_SERVICE", "none"),
            "online_stt": os.getenv("ONLINE_STT_SERVICE", "none"),
        },
        "vision": {
            "enabled": os.getenv("VISION_ENABLED", "true").lower() == "true",
            "camera": os.getenv("CAMERA_SOURCE", "mock"),
            "frame_width": int(os.getenv("FRAME_WIDTH", 640)),
            "frame_height": int(os.getenv("FRAME_HEIGHT", 480))
        },
        "memory": {
            "backend": os.getenv("MEMORY_BACKEND", "file"),
            "path": os.getenv("MEMORY_PATH", "./data/memory.json")
        },
        "hardware": {
            "gpio_enabled": os.getenv("GPIO_ENABLED", "true").lower() == "true",
            "motor_driver": os.getenv("MOTOR_DRIVER", "mock")
        },
        "llm": {
            "use_llm": os.getenv("USE_LLM", "false").lower() == "true",
            "mode": os.getenv("LLM_MODE", "offline"),
            "api_key": os.getenv("OPENAI_API_KEY", ""),
            "model": os.getenv("LLM_MODEL", "gpt-4")
        },
        "logging": {
            "level": os.getenv("LOG_LEVEL", "debug"),
            "to_file": os.getenv("LOG_TO_FILE", "false").lower() == "true"
        }
    }

def load_personality():
    path = os.path.join("syra", "personality", "personality.json")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Failed to load personality config: {e}")
        return {}

def load_config():
    config = load_env_config()
    config["personality"] = load_personality()
    return config