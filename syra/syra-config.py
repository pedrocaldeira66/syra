import json
import os

CONFIG_PATH = "personality/personality.json"

DEFAULT_PERSONALITY = {
    "name": "SYRA",
    "tone": "friendly",
    "formality": "casual",
    "values": ["curiosity", "empathy", "clarity"],
    "humor_level": 2,
    "safety_bias": "medium",
    "learning_style": "experience-based"
}

OPTIONS = {
    "tone": ["friendly", "neutral", "serious", "witty", "robotic"],
    "formality": ["casual", "moderate", "formal"],
    "safety_bias": ["low", "medium", "high"],
    "learning_style": ["experience-based", "instruction-based", "adaptive", "fixed"],
    "values": ["curiosity", "empathy", "clarity", "precision", "efficiency", "safety", "creativity"]
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_PERSONALITY.copy()
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(cfg):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=4)
    print("\nPersonality saved to", CONFIG_PATH)

def menu():
    config = load_config()

    while True:
        print("\nSYRA Personality Configuration")
        print("--------------------------------")
        for i, (key, value) in enumerate(config.items(), 1):
            print(f"{i}. {key}: {value}")
        print("0. Save and exit")
        print("9. Exit without saving")

        try:
            choice = int(input("\nSelect a field to edit: ").strip())
            if choice == 0:
                save_config(config)
                break
            elif choice == 9:
                print("\n[INFO] Changes discarded.")
                break
            elif 1 <= choice <= len(config):
                key = list(config.keys())[choice - 1]

                if key in OPTIONS:
                    options = OPTIONS[key]
                    print(f"\nChoose {key}:")
                    for idx, opt in enumerate(options, 1):
                        print(f"  {idx}. {opt}")

                    if key == "values":
                        selection = input(f"Enter comma-separated choices (e.g. 1,3,5) or press Enter to keep current: ").strip()
                        if not selection:
                            continue
                        try:
                            indices = [int(i) for i in selection.split(",")]
                            selected = [options[i-1] for i in indices if 1 <= i <= len(options)]
                            if selected:
                                config[key] = selected
                            else:
                                print("Invalid selection. No changes made.")
                        except:
                            print("Invalid input. No changes made.")
                    else:
                        default_index = options.index(config[key]) + 1
                        selected = input(f"Enter choice [1-{len(options)}] (default {default_index}): ").strip()
                        if not selected:
                            config[key] = options[default_index - 1]
                        elif selected.isdigit() and 1 <= int(selected) <= len(options):
                            config[key] = options[int(selected) - 1]
                        else:
                            print("Invalid selection. No changes made.")
                else:
                    new_val = input(f"Enter new value for '{key}' (current: {config[key]}): ").strip()
                    if not new_val:
                        print("Empty input not allowed.")
                        continue
                    if isinstance(config[key], int):
                        if new_val.isdigit():
                            config[key] = int(new_val)
                        else:
                            print("Invalid input. Expected a number.")
                    else:
                        config[key] = new_val
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    menu()