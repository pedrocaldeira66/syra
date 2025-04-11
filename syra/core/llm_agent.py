import os
from syra.config import load_config

config = load_config()
mode = config["llm"]["mode"]
model_name = config["llm"]["model"]
backend = config["llm"].get("backend", "llama-cpp")  # default offline engine
api_key = config["llm"].get("api_key")
provider = config["llm"].get("provider", "openai")   # for online fallback

# Basic mock fallback
class MockLLM:
    def ask(self, prompt):
        return f"[MOCK REPLY] You asked: {prompt}"

# Online LLM using OpenAI
def init_openai():
    import openai
    openai.api_key = api_key
    def ask(prompt):
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    return ask

# Offline LLM using llama-cpp-python
def init_llama_cpp():
    from llama_cpp import Llama
    model_path = os.path.join("models", f"{model_name}.gguf")
    llm = Llama(model_path=model_path, n_ctx=512, verbose=False)

    def ask(prompt):
        output = llm(prompt, max_tokens=256, stop=["</s>"])
        return output["choices"][0]["text"].strip()
    return ask

# Dispatcher
def initialize_llm():
    if config["use_mock"]:
        return MockLLM().ask

    if mode == "online":
        if provider == "openai" and api_key:
            return init_openai()
        else:
            print("[WARN] No supported online LLM provider configured.")
            return MockLLM().ask
    elif mode == "offline":
        if backend == "llama-cpp":
            return init_llama_cpp()
        else:
            print("[WARN] Unknown offline backend, using mock.")
            return MockLLM().ask
    else:
        print("[WARN] Unknown LLM mode.")
        return MockLLM().ask

# Expose LLM entry point
ask_llm = initialize_llm()