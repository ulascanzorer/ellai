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

def play_song(song_name: str) -> str:
    """
    Temporarily downloads a song from YouTube and plays it in the background using ffplay.
    
    Args:
        song_name (str): The name of the song to play.
        
    Returns:
        str: A message indicating the status of the playback.
    """
    import os
    import tempfile
    import subprocess

    try:
        import yt_dlp
    except ImportError:
        return "Error: yt-dlp is not installed. Please install it to use this tool."

    try:
        temp_dir = tempfile.gettempdir()
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, 'ellai_song_%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{song_name}", download=True)
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
            else:
                entry = info
            
            # The actual downloaded file path after ffmpeg processing will be mp3
            filename = ydl.prepare_filename(entry)
            filepath = os.path.splitext(filename)[0] + '.mp3'
            
        # Run ffplay in the background
        play_cmd = ["ffplay", "-nodisp", "-autoexit", filepath]
        subprocess.Popen(play_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        title = entry.get('title', song_name)
        return f"Successfully downloaded and currently playing '{title}' in the background."
    except Exception as e:
        return f"An error occurred while playing the song: {str(e)}"



EPHEMERAL_SCRIPT_PATH = "/tmp/ellai_ephemeral_script.py"

def ephemeral_creator(code: str, dependencies: list[str]) -> str:
    """
    Create a temporary Python script to be run by ephemeral_runner.

    Use this tool when the user asks for a task you cannot accomplish with
    your built-in tools. Write a complete Python script in `code` and list
    any required third-party packages in `dependencies`. The script is saved
    to a fixed temporary path with uv inline-script metadata prepended.
    Call ephemeral_runner immediately after to execute it.

    Args:
        code (str): The full Python script. Do NOT include a uv inline-script
            header — it is prepended automatically.
        dependencies (list[str]): PyPI package names needed by the script,
            e.g. ["requests", "pandas==2.2.0"]. Pass [] if none are needed.

    Returns:
        str: Confirmation that the script was saved, or an error message.

    Example usage:
        ephemeral_creator(
            code="import requests\nprint(requests.get('https://example.com').status_code)",
            dependencies=["requests"]
        )
    """
    try:
        dep_lines = "\n".join(f'#   "{dep}",' for dep in dependencies)
        if dep_lines:
            header = (
                "# /// script\n"
                '# requires-python = ">=3.10"\n'
                "# dependencies = [\n"
                f"{dep_lines}\n"
                "# ]\n"
                "# ///\n\n"
            )
        else:
            header = (
                "# /// script\n"
                '# requires-python = ">=3.10"\n'
                "# dependencies = []\n"
                "# ///\n\n"
            )

        with open(EPHEMERAL_SCRIPT_PATH, "w") as f:
            f.write(header + code)

        return f"Ephemeral script saved to {EPHEMERAL_SCRIPT_PATH}. Call ephemeral_runner to execute it."
    except Exception as e:
        return f"Error saving ephemeral script: {str(e)}"


def ephemeral_runner() -> str:
    """
    Execute the ephemeral script previously created by ephemeral_creator.

    Runs the script using `uv run`, which automatically installs any
    inline-declared dependencies into an isolated environment. Captures
    stdout and stderr. Times out after 30 seconds.

    Returns:
        str: The exit code, stdout, and stderr of the script, clearly
            labelled. Returns an error message if the script does not exist,
            times out, or `uv` is not found on PATH.

    Example usage:
        ephemeral_runner()
    """
    import os
    import subprocess

    if not os.path.exists(EPHEMERAL_SCRIPT_PATH):
        return (
            f"Error: No ephemeral script found at {EPHEMERAL_SCRIPT_PATH}. "
            "Call ephemeral_creator first."
        )

    try:
        result = subprocess.run(
            ["uv", "run", EPHEMERAL_SCRIPT_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )
        stdout = result.stdout.strip() or "(empty)"
        stderr = result.stderr.strip() or "(empty)"
        return (
            f"[exit code: {result.returncode}]\n\n"
            f"[stdout]\n{stdout}\n\n"
            f"[stderr]\n{stderr}"
        )
    except subprocess.TimeoutExpired:
        return "Error: Ephemeral script timed out after 30 seconds."
    except FileNotFoundError:
        return "Error: `uv` executable not found. Ensure uv is installed and on PATH."
    except Exception as e:
        return f"Error running ephemeral script: {str(e)}"