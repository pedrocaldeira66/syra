import os
import json
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = os.getenv("CONFIG_FILE", "core/config/hardware_config.json")


def load_config():
    config = {
        "hardware": {},
        "personality": {},
        "llm": {},
        "mode": {},
    }

    # Load hardware config from JSON if available
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config["hardware"] = json.load(f)

    # Load personality from .env
    config["personality"]["tone"] = os.getenv("SYRA_TONE", "warm")
    config["personality"]["formality"] = os.getenv("SYRA_FORMALITY", "casual")
    config["personality"]["name"] = os.getenv("SYRA_NAME", "SYRA")
    config["personality"]["creator_name"] = os.getenv("CREATOR_NAME", "The Creator")

    # Load mode defaults from .env
    config["mode"]["LLM_MODE"] = os.getenv("LLM_MODE", "offline")
    config["mode"]["TTS_MODE"] = os.getenv("TTS_MODE", "offline")
    config["mode"]["STT_MODE"] = os.getenv("STT_MODE", "offline")

    # Load LLM config from .env
    config["llm"]["model"] = os.getenv("LLM_MODEL")
    config["llm"]["api_key"] = os.getenv("LLM_API_KEY")
    config["llm"]["endpoint"] = os.getenv("LLM_API_URL")
    config["llm"]["provider"] = os.getenv("LLM_PROVIDER")

    # Fallback: load servo values from .env if hardware config is missing or incomplete
    if "servos" not in config["hardware"]:
        config["hardware"]["servos"] = {
            "LEFT_EYE_H": int(os.getenv("LEFT_EYE_H_SERVO", 0)),
            "LEFT_EYE_V": int(os.getenv("LEFT_EYE_V_SERVO", 1)),
            "RIGHT_EYE_H": int(os.getenv("RIGHT_EYE_H_SERVO", 2)),
            "RIGHT_EYE_V": int(os.getenv("RIGHT_EYE_V_SERVO", 3)),
            "MOUTH": int(os.getenv("MOUTH_SERVO", 4)),
            "LEFT_UPPER_LID": int(os.getenv("LEFT_UPPER_LID_SERVO", 5)),
            "RIGHT_UPPER_LID": int(os.getenv("RIGHT_UPPER_LID_SERVO", 6)),
        }

    # Fallback for PCA9685 address
    if "pca9685_address" not in config["hardware"]:
        config["hardware"]["pca9685_address"] = os.getenv("PCA9685_ADDRESS", "0x40")

    return config


config = load_config()
