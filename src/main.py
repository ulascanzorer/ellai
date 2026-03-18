from src.core.ellai import Ellai
from src.core.utils import load_system_prompt

if __name__ == "__main__":
    ellai = Ellai(system_prompt=load_system_prompt())
    print("Ellai is ready! Type 'quit' or 'exit' to stop chatting.")

    while True:
        try:
            user_input = input("You: ")
            if user_input.strip().lower() in ["quit", "exit"]:
                break

            if not user_input.strip():
                continue

            print("Ellai: ", end="", flush=True)
            ellai.chat_cli_streaming(message=user_input, enable_thinking=False)
            print("\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break