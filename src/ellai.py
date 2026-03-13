from ollama import chat, ChatResponse, web_fetch, web_search
from typing import Optional
from custom_tools import add_to_memory

class Ellai:
    """Ellai is a chatbot that can answer questions and provide information."""
    
    def __init__(
        self,
        model: str = "qwen3.5:4b",
        system_prompt: str = "Your name is Ellai. You are a helpful assistant. You MUST ALWAYS answer like a pirate.",
    ):
        """Initialize the Ellai chatbot."""
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

    def chat_cli(self, message: str, enable_thinking: bool = False, debug: bool = False) -> Optional[str]:
        """Send a message and return the final text response, excluding thinking and tool calling content."""
        
        self.messages.append({"role": "user", "content": message})

        while True:
            response: ChatResponse = chat(model=self.model, messages=self.messages, tools=self.available_tools.values(), think=enable_thinking, options=self.model_options)
            self.messages.append(response.message)

            if response.message.thinking:
                if debug:
                    print(f"Thinking: {response.message.thinking}")
            if response.message.content:
                if debug:
                    print(f"Content: {response.message.content}")
                return response.message.content
            if response.message.tool_calls:
                if debug:
                    tool_calls_str = f"Tool calls: {response.message.tool_calls}"
                    print(tool_calls_str)
                for tool_call in response.message.tool_calls:
                    function_to_call = self.available_tools.get(tool_call.function.name)
                    if function_to_call:
                        args = tool_call.function.arguments
                        result = function_to_call(**args)
                        if debug:
                            result_str = f"Result: {str(result)[:200]}..."
                            print(result_str)
                        # Result is truncated for limited context lengths.
                        self.messages.append({"role": "tool", "content": str(result)[:4000 * 4], "tool_name": tool_call.function.name})
                    else:
                        self.messages.append({"role": "tool", "content": f"Tool {tool_call.function.name} not found", "tool_name": tool_call.function.name})
            else:
                break

    def chat_cli_streaming(self, message: str, enable_thinking: bool = False, debug: bool = False):
        """Chat with Ellai in a streaming fashion as documented by ollama."""
        
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
                    result = str(result)[:20000]    # Again cutting off the result to not occupy too much of the context window.
                else:
                    result = "Unknown tool"

                self.messages.append({"role": "tool", "tool_name": call.function.name, "content": result})

    def reset(self):
        """Reset Ellai's conversation history."""
        self.messages = []