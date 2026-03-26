# ellai

![version](https://img.shields.io/github/v/release/ulascanzorer/ellai?label=version)

Ellai is a personal AI assistant running locally in the terminal, powered by [Ollama](https://ollama.com/) and local LLMs. It features a persistent memory system, web search capabilities, and the ability to dynamically write and run Python programs to accomplish tasks it couldn't handle otherwise.

## Features

- **Interactive Terminal Interface**: Chat with Ellai directly from your terminal.
- **Persistent Memory**: Remembers user details, preferences, and context across sessions by saving them to `ellai_memory.md`.
- **Tool Calling Capabilities**:
  - `web_search`: Search the web for real-time information.
  - `web_fetch`: Fetch content from specific URLs.
  - `add_to_memory`: Persist important information.
  - `play_song`: Download and play a song from YouTube in the background.
  - `ephemeral_creator`: Write a Python script with any required dependencies and save it to a temp path.
  - `ephemeral_runner`: Execute the previously created script via `uv run`, with dependencies auto-installed.
- **Thinking Process**: Supports model "thinking" / Chain-of-Thought (CoT) processes for supported models.

## How to Use

### Prerequisites
- **Python**: Version 3.10 or higher.
- **uv**: Required to manage dependencies and run the project. Install it from [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/). Also required at runtime for the `ephemeral_creator`/`ephemeral_runner` tools.
- **Ollama**: Must be installed and running locally. You can download and install it from [ollama.com/download](https://ollama.com/download).
- **Tool Calling Model**: Since Ellai actively relies on tools for memory and web access, the model used in Ollama *must* support tool calling. The default model is `qwen3.5:4b`.
- **API Key**: A free API key from Ollama is needed for the `web_search` and `web_fetch` features to work properly. Ensure you have obtained and configured it.
- **ffmpeg / ffplay** *(optional)*: Required for the `play_song` tool. Install via your system package manager (e.g. `sudo pacman -S ffmpeg` or `sudo apt install ffmpeg`).

### Installation & Running

Start a chat in the terminal by running:
```bash
uv run python -m src.main
```

Alternatively, you can run the Gradio web application:
```bash
uv run python -m src.gradio.gradio_app
```
