from syra.config import load_config
from syra.core.llm.llm_agent import ask_llm

config = load_config()
use_llm = config.get("llm", {}).get("use_llm", False)

def analyze(prompt):
    if not use_llm:
        print("[REASONING] LLM disabled, using default response.")
        return "I'm not currently processing reasoning tasks."

    print(f"[REASONING] Prompt received: {prompt}")
    try:
        response = ask_llm(prompt)
        print(f"[REASONING] LLM response: {response}")
        return response
    except Exception as e:
        print(f"[ERROR] Reasoning failed: {e}")
        return "An error occurred during reasoning."

# Optional: test run
if __name__ == "__main__":
    print(analyze("What is the mission objective?"))