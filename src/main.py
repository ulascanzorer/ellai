from ellai import Ellai

if __name__ == "__main__":
    ellai = Ellai()
    print("Ellai is ready! Type 'quit' or 'exit' to stop chatting.")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.strip().lower() in ['quit', 'exit']:
                break

            if not user_input.strip():
                continue

            response = ellai.chat(user_input)
            print(f"Ellai: {response}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break