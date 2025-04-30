import re
import requests
import feedparser
import streamlit as st


def is_valid_youtube_url(url: str) -> bool:
    """
    Returns True if the provided URL is exactly in the format:
      https://www.youtube.com/watch?v=VIDEO_ID&
    where VIDEO_ID is exactly 11 characters (letters, numbers, '-' or '_'),
    and the URL ends with an ampersand.
    """
    pattern = r"^https://www\.youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})(?:&.*)?$"
    return re.match(pattern, url) is not None


def is_valid_rss_feed_url(url: str) -> bool:
    """
    Checks if the given URL is accessible by making an HTTP GET request.

    Parameters:
    - url (str): The RSS feed URL to validate.

    Returns:
    - bool: True if the URL returns a 200 OK response, False otherwise.
    """
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def is_rss_feed_episode_valid(source_url: str, episode_name: str) -> bool:
    """
    Checks if a given episode name exists in the RSS feed.

    Parameters:
    - source_url (str): The URL of the RSS feed.
    - episode_name (str): The title of the episode to search for.

    Returns:
    - bool: True if an episode with the given name exists in the feed, False otherwise.
    """
    feed = feedparser.parse(source_url)
    for entry in feed.entries:
        if episode_name.lower() == entry.title.lower():
            return True
    return False


def show_succesfully_downloaded(title: str):
    """
    Displays a success message for a downloaded episode.

    Parameters:
    - title (str): The episode title.
    """
    st.subheader("✅ Downloaded")
    st.write("Episode name:")
    st.write(title)
    st.divider()


def show_succesfully_transcribed():
    """Displays a success message for a completed transcription."""
    st.subheader("✅ Transcribed")
    st.divider()


def show_succesfully_summarized(text: str):
    """
    Displays a success message for a completed summary.

    Parameters:
    - text (str): The summarized text.
    """
    st.subheader("✅ Summarized")
    st.markdown(text)
    st.divider()
