import os
import json
import logging

from typing import Tuple
from yt_dlp import YoutubeDL
from downloader import Downloader
from utils.youtube_utils import extract_video_id, extract_video_url, get_ydl_opts

logger = logging.getLogger(__name__)

MP3_EXTENSION = ".mp3"
YOUTUBE_DIR = "youtube"
DOWNLOADS_DIR = "downloads"
METADATA_EXTENSION = ".info.json"
OUTPUT_DIR = os.path.join(DOWNLOADS_DIR, YOUTUBE_DIR)


class YouTube_Downloader(Downloader):
    """Downloads YouTube videos as MP3 and retrieves metadata."""

    def __init__(self, config: dict):
        self.config = config
        self.debug = self.config.get("DEBUG", False)

    def download_mp3(self) -> str:
        """Downloads the video as an MP3 file."""
        return self._download_file(extension=MP3_EXTENSION, audio_only=True)

    def download_metadata(self) -> dict:
        """Downloads video metadata as a JSON file and returns its contents."""
        metadata_path = self._download_file(extension=METADATA_EXTENSION)

        try:
            with open(metadata_path, "r", encoding="utf8") as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Failed to read metadata file: {e}")
            return {}

    def download_episode(
        self, source_url: str, episode_name: str | None
    ) -> Tuple[str, str, str]:
        """Downloads both the MP3 file and metadata, then logs key details."""
        self.source_url = extract_video_url(source_url=source_url)
        self.video_id = extract_video_id(source_url=self.source_url)

        if self.debug:
            logger.info(f"Video ID is: {self.video_id}")
            logger.info(f"Video URL is: {self.source_url}")

        mp3_path = self.download_mp3()
        metadata = self.download_metadata()

        if self.debug:
            logger.info(
                f"Video length: {metadata.get('duration', 0) / 60:.2f} minutes."
            )

        return mp3_path, metadata.get("title", ""), self.video_id

    def _download_file(self, extension: str, audio_only: bool = False) -> str:
        """Handles downloading the requested file type."""
        output_path = os.path.join(
            os.getcwd(), OUTPUT_DIR, self.video_id, f"{self.video_id}{extension}"
        )

        if os.path.exists(output_path):
            if self.debug:
                logger.info(f"File already exists ({extension}).")
            return output_path

        with YoutubeDL(get_ydl_opts(OUTPUT_DIR, audio_only)) as ydl:
            try:
                ydl.download([self.source_url])
            except Exception as e:
                logger.error(f"Failed to download {extension}: {e}")
                raise

        if self.debug:
            logger.info(f"Successfully downloaded file ({extension}).")

        return output_path
