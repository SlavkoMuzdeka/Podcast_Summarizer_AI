import os
import feedparser
import requests

CHUNK_SIZE = 8192
OUTPUT_DIR = os.path.join(os.getcwd(), "downloads", "rss")


class RSSDownloader:
    def download_episode(self, rss_url: str, episode_name: str) -> str:
        entry = self._get_episode_entry(rss_url, episode_name)

        if not entry:
            raise ValueError("Episode not found. Please check the episode name.")

        if "enclosures" not in entry and not entry.enclosures:
            raise ValueError("No audio enclosure available.")

        mp3_url = entry.enclosures[0].href
        episode_id = self._extract_episode_id(mp3_url)
        os.makedirs(os.path.join(OUTPUT_DIR, episode_id), exist_ok=True)
        file_path = os.path.join(OUTPUT_DIR, episode_id, episode_id + ".mp3")

        if os.path.exists(file_path):
            print("Episode already downloaded.")
            return file_path

        response = requests.get(mp3_url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                file.write(chunk)

        return file_path

    def _get_episode_entry(self, rss_url: str, episode_name: str):
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            if episode_name.lower() == entry.title.lower():
                return entry
        return None

    def _extract_episode_id(self, mp3_url: str) -> str:
        return mp3_url.split("/")[-1].split(".")[0]
