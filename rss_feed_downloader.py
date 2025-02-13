import os
import logging
import requests
from utils.rss_feed_utils import extract_episode_id, get_episode_entry

logger = logging.getLogger(__name__)

CHUNK_SIZE = 8192
RSS_FEED_DIR = "rss"
MP3_EXTENSION = ".mp3"
DOWNLOADS_DIR = "downloads"
OUTPUT_DIR = os.path.join(os.getcwd(), DOWNLOADS_DIR, RSS_FEED_DIR)


class RSS_Feed_Downloader:
    """
    A class for downloading podcast episodes from an RSS feed.

    Attributes:
        config (dict): Configuration settings, including debug mode.
        debug (bool): Flag indicating whether debug logging is enabled.
    """

    def __init__(self, config: dict):
        """
        Initializes the RSS_Feed_Downloader with the given configuration.

        Parameters:
            config (dict): Configuration dictionary, where "DEBUG" can be set to True for logging.
        """
        self.config = config
        self.debug = self.config.get("DEBUG", False)

    def download_episode(self, source_url: str, episode_name: str | None) -> str:
        """
        Downloads a podcast episode from the given RSS feed URL.

        Parameters:
            source_url (str): The URL of the RSS feed.
            episode_name (str | None): The name of the episode to download. If None, defaults to the latest episode.

        Returns:
            tuple: (file_path (str), episode_name (str), episode_id (str)) if successful.

        Raises:
            ValueError: If the episode is not found or no audio file is available.
        """
        # Retrieve episode details
        entry = get_episode_entry(source_url, episode_name)

        if not entry:
            raise ValueError("Episode not found. Please check the episode name.")

        if "enclosures" not in entry and not entry.enclosures:
            raise ValueError("No audio enclosure available.")

        # Extract episode URL and generate filename
        mp3_url = entry.enclosures[0].href
        episode_id = extract_episode_id(mp3_url)
        os.makedirs(os.path.join(OUTPUT_DIR, episode_id), exist_ok=True)
        file_path = os.path.join(OUTPUT_DIR, episode_id, episode_id + MP3_EXTENSION)

        # Check if the episode is already downloaded
        if os.path.exists(file_path):
            if self.debug:
                logger.info("Episode already downloaded.")
            return file_path, episode_name, episode_id

        # Download the episode in chunks
        response = requests.get(mp3_url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                file.write(chunk)

        if self.debug:
            logger.info("Successfully downloaded episode.")

        return file_path, episode_name, episode_id
