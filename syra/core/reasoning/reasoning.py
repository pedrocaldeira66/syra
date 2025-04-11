from syra.config import load_config
from syra.core.llm.llm_agent import ask_llm
from syra.core.memory.memory import save_interaction
from syra.core.memory.memory_index import search_memory, summarize_results
from syra.core.memory.knowledge_store import load_knowledge

config = load_config()
USE_LLM = config.get("use_llm", False)
INJECT_MEMORY = config.get("reasoning", {}).get("inject_memory", True)

def build_context(prompt):
    context = ""

    # Recall similar memory
    if INJECT_MEMORY:
        matches = search_memory(prompt)
        if matches:
            context += "Past related conversations:\n"
            context += summarize_results(matches)
            context += "\n\n"

    # Inject known facts
    knowledge = load_knowledge()
    if knowledge:
        context += "Known facts:\n"
        for key, val in knowledge.items():
            context += f"- {key}: {val}\n"
        context += "\n"

    return context + f"User: {prompt}"

def analyze(prompt: str) -> str:
    if not USE_LLM:
        return "LLM disabled. I'm only listening."

    try:
        full_prompt = build_context(prompt)
        response = ask_llm(full_prompt)
        save_interaction(prompt, response)
        return response
    except Exception as e:
        print(f"[REASONING ERROR] {e}")
        return "Sorry, something went wrong while thinking."