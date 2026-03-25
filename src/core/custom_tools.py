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