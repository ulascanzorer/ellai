from ellai import Ellai
from system_prompt_template import SYSTEM_PROMPT_TEMPLATE

def load_system_prompt() -> str:
    memory_path = "./ellai_memory.md"
    try:
        with open(memory_path, "r") as f:
            memory = f.read().strip()
    except FileNotFoundError:
        memory = "No memories saved yet."
    
    return SYSTEM_PROMPT_TEMPLATE.format(memory=memory)

if __name__ == "__main__":
    system_prompt = load_system_prompt()
    ellai = Ellai(system_prompt=system_prompt)
    print("Ellai is ready! Type 'quit' or 'exit' to stop chatting.")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.strip().lower() in ["quit", "exit"]:
                break

            if not user_input.strip():
                continue

            response = ellai.chat(user_input)
            print(f"\nEllai: {response}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break