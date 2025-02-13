import feedparser


def get_episode_entry(source_url: str, episode_name: str):
    """
    Retrieves an episode entry from an RSS feed.

    Parameters:
        source_url (str): The URL of the RSS feed.
        episode_name (str): The name of the episode to find.

    Returns:
        dict or None: The episode entry if found, otherwise None.
    """
    feed = feedparser.parse(source_url)
    for entry in feed.entries:
        if episode_name.lower() == entry.title.lower():
            return entry
    return None


def extract_episode_id(mp3_url: str) -> str:
    """
    Extracts the episode ID from an MP3 URL.

    Parameters:
        mp3_url (str): The direct URL of the MP3 file.

    Returns:
        str: The extracted episode ID (typically the filename without the extension).
    """
    return mp3_url.split("/")[-1].split(".")[0]
