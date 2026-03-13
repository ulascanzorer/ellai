from ellai import Ellai
from utils import load_system_prompt

if __name__ == "__main__":
    ellai = Ellai(system_prompt=load_system_prompt())
    print("Ellai is ready! Type 'quit' or 'exit' to stop chatting.")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.strip().lower() in ["quit", "exit"]:
                break

            if not user_input.strip():
                continue

            response = ellai.chat_cli(message=user_input)
            print(f"\nEllai: {response}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break