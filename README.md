# ellai

![version](https://img.shields.io/github/v/release/ulascanzorer/ellai?label=version)

Ellai is a personal AI assistant running locally in the terminal, powered by [Ollama](https://ollama.com/) and local LLMs. It features a persistent memory system and web search capabilities.

## Features

- **Interactive Terminal Interface**: Chat with Ellai directly from your terminal.
- **Persistent Memory**: Remembers user details, preferences, and context across sessions by saving them to `ellai_memory.md`.
- **Tool Calling Capabilities**:
  - `web_search`: Search the web for real-time information.
  - `web_fetch`: Fetch content from specific URLs.
  - `add_to_memory`: Persist important information.
- **Thinking Process**: Supports model "thinking" / Chain-of-Thought (CoT) processes for supported models.

## How to Use

### Prerequisites
- **Python**: Version 3.10 or higher.
- **Ollama**: Must be installed and running locally. You can download and install it from [ollama.com/download](https://ollama.com/download).
- **Tool Calling Model**: Since Ellai actively relies on tools for memory and web access, the model used in Ollama *must* support tool calling. The default model is `qwen3.5:4b`.
- **API Key**: A free API key from Ollama is needed for the `web_search` and `web_fetch` features to work properly. Ensure you have obtained and configured it.

### Installation & Running

We recommend using [uv](https://github.com/astral-sh/uv) to manage dependencies and run the project.

Start a chat in the terminal by running:
```bash
uv run python -m src.main
```

Alternatively, you can run the Gradio web application:
```bash
uv run python -m src.gradio.gradio_app
```
