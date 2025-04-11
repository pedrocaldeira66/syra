from syra.config import load_config
from syra.core.llm.llm_agent import ask_llm

config = load_config()
USE_LLM = config.get("use_llm", False)

def analyze(prompt: str) -> str:
    if not USE_LLM:
        print("[REASONING] LLM is disabled in config. Returning fallback response.")
        return "I'm not currently processing reasoning tasks."

    print(f"[REASONING] Analyzing input: {prompt}")
    try:
        response = ask_llm(prompt)
        print(f"[REASONING] LLM response: {response}")
        return response
    except Exception as e:
        print(f"[REASONING ERROR] {e}")
        return "An error occurred during reasoning."