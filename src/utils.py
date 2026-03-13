from system_prompt_template import SYSTEM_PROMPT_TEMPLATE

def load_system_prompt() -> str:
    memory_path = "./ellai_memory.md"
    try:
        with open(memory_path, "r") as f:
            memory = f.read().strip()
    except FileNotFoundError:
        memory = "No memories saved yet."
    return SYSTEM_PROMPT_TEMPLATE.format(memory=memory)