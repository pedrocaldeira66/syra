import os
import json
import requests
from syra.config import load_config

config = load_config()
mode = config.get("llm", {}).get("mode", "offline")
model_name = config.get("llm", {}).get("model", "gpt4all-mistral")
backend = config.get("llm", {}).get("backend", "llama-cpp")
api_key = config.get("llm", {}).get("api_key")
api_url = config.get("llm", {}).get("api_url")
headers = config.get("llm", {}).get("headers")
body_template = config.get("llm", {}).get("body_template")

class MockLLM:
    def ask(self, prompt):
        return f"[MOCK REPLY] You said: {prompt}"

def init_llama_cpp():
    from llama_cpp import Llama
    model_path = os.path.join("models", f"{model_name}.gguf")
    llm = Llama(model_path=model_path, n_ctx=512, verbose=False)

    def ask(prompt):
        output = llm(prompt, max_tokens=256, stop=["</s>"])
        return output["choices"][0]["text"].strip()
    return ask

def init_api_request():
    if not (api_url and api_key and headers and body_template):
        print("[LLM] Missing API config. Falling back to mock.")
        return MockLLM().ask

    try:
        parsed_headers = json.loads(headers.replace("$API_KEY", api_key))
        parsed_body_template = json.loads(body_template)

        def ask(prompt):
            body = json.loads(json.dumps(parsed_body_template).replace("$MODEL", model_name).replace("$PROMPT", prompt))
            response = requests.post(api_url, headers=parsed_headers, json=body)
            content = response.json()
            return (
                content.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "[No reply]")
                .strip()
            )
        return ask

    except Exception as e:
        print(f"[LLM ERROR] Failed to init online LLM: {e}")
        return MockLLM().ask

def initialize_llm():
    if config.get("use_mock", False):
        return MockLLM().ask

    if mode == "offline":
        if backend == "llama-cpp":
            return init_llama_cpp()
        else:
            print(f"[LLM] Unsupported offline backend: {backend}")
            return MockLLM().ask
    elif mode == "online":
        return init_api_request()
    else:
        print("[LLM] Unknown LLM mode.")
        return MockLLM().ask

ask_llm = initialize_llm()