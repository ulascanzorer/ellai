def add_to_memory(content_to_add: str) -> None:
    """
    Persist important information to Ellai's long-term memory file.

    Use this tool whenever the user shares information that should be remembered
    across future conversations, such as:
      - Personal details (name, preferences, goals, habits)
      - Facts or context the user explicitly wants remembered
      - Important decisions, plans, or agreements made during the conversation
      - Any information the user says like "remember that..." or "keep in mind..."

    The memory is stored as a Markdown file (`ellai_memory.md`) in the current
    working directory. Each call appends to the end of the file, so previously
    saved memories are never overwritten.

    Args:
        content_to_add (str): The information to store in memory. Should be a
            clear, self-contained note written in a way that will still make
            sense when read back in a future conversation. Prefer complete
            sentences or labeled key-value lines (e.g. "User's name: Alice").

    Returns:
        None

    Example usage:
        add_to_memory("User's name is Alex and they prefer concise responses.")
        add_to_memory("User is training for a marathon starting March 2026.")
    """
    memory_path = "./ellai_memory.md"
    with open(memory_path, "a") as file:
        file.write(content_to_add + "\n")