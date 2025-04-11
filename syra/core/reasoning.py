import os
from dotenv import load_dotenv

load_dotenv()

USE_LLM = os.getenv("USE_LLM", "false").lower() == "true"
LLM_MODE = os.getenv("LLM_MODE", "offline")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

class ReasoningEngine:
    def __init__(self):
        self.use_llm = USE_LLM and LLM_MODE == "online" and bool(OPENAI_API_KEY)
        if self.use_llm:
            import openai
            openai.api_key = OPENAI_API_KEY
            self.client = openai
        else:
            self.client = None

    def generate_plan(self, perception, memory):
        if self.use_llm:
            try:
                prompt = f"Perception: {perception}\nMemory: {memory}\nWhat should I do?"
                response = self.client.ChatCompletion.create(
                    model=LLM_MODEL,
                    messages=[{"role": "user", "content": prompt}]
                )
                plan = response["choices"][0]["message"]["content"]
                return {"plan": plan}
            except Exception as e:
                print(f"[LLM ERROR] {e}")
                return {"plan": "error"}
        else:
            return {"plan": "say hi"}  # Simple placeholder logic

    def select_action(self, plan):
        return plan["plan"]

def initialize(config):
    print(f"[INIT] Reasoning engine initialized. LLM={'enabled' if USE_LLM else 'disabled'}, MODE={LLM_MODE}")
