from ollama import chat
from ollama import ChatResponse
from typing import Optional

class Ellai:
    """Ellai is a chatbot that can answer questions and provide information."""
    
    def __init__(
        self,
        model: str = "llama3.2",
        system_prompt: str = "Your name is Ellai. You are a helpful assistant.",
    ):
        """Initialize the Ellai chatbot."""
        self.model     = model
        self.messages  = [{"role": "system", "content": system_prompt}]

    def chat(self, message: str) -> Optional[str]:
        """Send a message and return the text response."""
        self.messages.append({"role": "user", "content": message})
        response: ChatResponse = chat(model=self.model, messages=self.messages)
        reply = response.message.content
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def reset(self):
        """Reset the Ellai's conversation history."""
        self.messages = []