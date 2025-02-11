import os
import logging
import requests
import feedparser

logger = logging.getLogger(__name__)

CHUNK_SIZE = 8192
RSS_FEED_DIR = "rss"
MP3_EXTENSION = ".mp3"
DOWNLOADS_DIR = "downloads"
OUTPUT_DIR = os.path.join(os.getcwd(), MP3_EXTENSION, DOWNLOADS_DIR)


class RSS_Downloader:
    def __init__(self, debug: bool):
        self.debug = debug

    def download_episode(self, source_url: str, episode_name: str | None) -> str:
        entry = self._get_episode_entry(source_url, episode_name)

        if not entry:
            raise ValueError("Episode not found. Please check the episode name.")

        if "enclosures" not in entry and not entry.enclosures:
            raise ValueError("No audio enclosure available.")

        mp3_url = entry.enclosures[0].href
        episode_id = self._extract_episode_id(mp3_url)
        os.makedirs(os.path.join(OUTPUT_DIR, episode_id), exist_ok=True)
        file_path = os.path.join(OUTPUT_DIR, episode_id, episode_id + MP3_EXTENSION)

        if os.path.exists(file_path):
            if self.debug:
                logger.info("Episode already downloaded.")
            return file_path

        response = requests.get(mp3_url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                file.write(chunk)

        if self.debug:
            logger.info("Successfully downloaded episode.")

        return file_path

    def _get_episode_entry(self, source_url: str, episode_name: str):
        feed = feedparser.parse(source_url)
        for entry in feed.entries:
            if episode_name.lower() == entry.title.lower():
                return entry
        return None

    def _extract_episode_id(self, mp3_url: str) -> str:
        return mp3_url.split("/")[-1].split(".")[0]
