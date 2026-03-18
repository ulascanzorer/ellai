from ollama import chat, web_fetch, web_search
from src.core.custom_tools import add_to_memory

class Ellai:
    """Ellai is a chatbot that can answer questions and provide information."""
    
    def __init__(
        self,
        model: str = "qwen3.5:4b",
        system_prompt: str = "Your name is Ellai. You are a helpful assistant. You MUST ALWAYS answer like a pirate.",
    ):
        """Initialize Ellai."""
        self.model = model
        self.messages = [{"role": "system", "content": system_prompt}]
        self.available_tools = {
            "web_fetch": web_fetch,
            "web_search": web_search,
            "add_to_memory": add_to_memory
        }
        
        # These options are considered to be optimal when the model is used in non-thinking mode, for general tasks: https://huggingface.co/Qwen/Qwen3.5-4B.
        self.model_options = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 20,
            "min_p": 0.0,
            "presence_penalty": 1.5,
            "repetition_penalty": 1.0
        }

    def chat_cli_streaming(self, message: str, enable_thinking: bool = False, debug: bool = False):
        """Chat with Ellai in a streaming fashion as documented by ollama: https://docs.ollama.com/capabilities/tool-calling."""
        
        self.messages.append({"role": "user", "content": message})

        while True:
            stream = chat(model=self.model, messages=self.messages, tools=self.available_tools.values(), stream=True, think=enable_thinking, options=self.model_options)

            thinking = ""
            content = ""
            tool_calls = []

            done_thinking = False

            for chunk in stream:
                if chunk.message.thinking:
                    thinking += chunk.message.thinking
                    print(chunk.message.thinking, end="", flush=True)
                if chunk.message.content:
                    if not done_thinking:
                        done_thinking = True
                        print("\n")
                    content += chunk.message.content
                    print(chunk.message.content, end="", flush=True)
                if chunk.message.tool_calls:
                    tool_calls.extend(chunk.message.tool_calls)
                    if debug:
                        print(chunk.message.tool_calls)

            if thinking or content or tool_calls:
                self.messages.append({"role": "assistant", "thinking": thinking, "content": content, "tool_calls": tool_calls})

            if not tool_calls:
                break

            for call in tool_calls:
                function_to_call = self.available_tools.get(call.function.name)
                if function_to_call:
                    result = function_to_call(**call.function.arguments)
                    result = str(result)[:20000]    # Cutting off the result by an arbitrary length to not occupy too much of the context window.
                else:
                    result = "Unknown tool"

                self.messages.append({"role": "tool", "tool_name": call.function.name, "content": result})

    def reset(self):
        """Reset Ellai's conversation history."""
        self.messages = []