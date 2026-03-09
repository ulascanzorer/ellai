from ollama import chat, ChatResponse, web_fetch, web_search
from typing import Optional

class Ellai:
    """Ellai is a chatbot that can answer questions and provide information."""
    
    def __init__(
        self,
        model: str = "qwen3.5:4b",
        system_prompt: str = "Your name is Ellai. You are a helpful assistant.",
    ):
        """Initialize the Ellai chatbot."""
        self.model = model
        self.messages = [{"role": "system", "content": system_prompt}]
        self.available_tools = {
            "web_fetch": web_fetch,
            "web_search": web_search,
        }

    def chat(self, message: str, debug: bool = False) -> Optional[str]:
        """Send a message and return the text response."""
        final_response = ""
        self.messages.append({"role": "user", "content": message})

        while True:
            response: ChatResponse = chat(model=self.model, messages=self.messages, tools=list(self.available_tools.values()), think=True)

            if response.message.thinking:
                if debug:
                    print(f"Thinking: {response.message.thinking}")
            if response.message.content:
                if debug:
                    print(f"Content: {response.message.content}")
                final_response += response.message.content
                self.messages.append(response.message)
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
                        # Result is truncated for limited context lengths
                        self.messages.append({"role": "tool", "content": str(result)[:4000 * 4], "tool_name": tool_call.function.name})
                    else:
                        self.messages.append({"role": "tool", "content": f"Tool {tool_call.function.name} not found", "tool_name": tool_call.function.name})
            else:
                break

        return final_response

    def reset(self):
        """Reset the Ellai's conversation history."""
        self.messages = []