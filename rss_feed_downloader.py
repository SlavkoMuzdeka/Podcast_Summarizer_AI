import os
import logging
import requests
import feedparser

logger = logging.getLogger(__name__)


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
        self.debug = self.config.get("debug", False)

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
        entry = self._get_episode_entry(source_url, episode_name)

        if not entry:
            raise ValueError("Episode not found. Please check the episode name.")

        if "enclosures" not in entry and not entry.enclosures:
            raise ValueError("No audio enclosure available.")

        # Extract episode URL and generate filename
        mp3_url = entry.enclosures[0].href
        episode_id = mp3_url.split("/")[-1].split(".")[0]

        output_dir = os.path.join(
            os.getcwd(), self.config.get("downloads_dir", "downloads"), episode_id
        )
        os.makedirs(os.path.join(output_dir, episode_id), exist_ok=True)
        file_path = os.path.join(
            output_dir, episode_id, episode_id + self.config.get("mp3_ext", ".mp3")
        )

        if self.debug and os.path.exists(file_path):
            logger.info("Episode already downloaded.")
            return file_path, episode_name, episode_id

        # Download the episode in chunks
        response = requests.get(mp3_url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(
                chunk_size=self.config.get("chunk_size", 8192)
            ):
                file.write(chunk)

        if self.debug:
            logger.info("Successfully downloaded episode.")

        return file_path, episode_name, episode_id

    def _get_episode_entry(self, source_url: str, episode_name: str):
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
