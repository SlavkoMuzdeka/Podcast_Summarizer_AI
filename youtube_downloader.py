import os
import json
import logging

from typing import Tuple
from yt_dlp import YoutubeDL
from downloader import Downloader

# Set up logging
logger = logging.getLogger(__name__)

# Constants
MP3_EXTENSION = ".mp3"
METADATA_EXTENSION = ".info.json"
OUTPUT_DIR = os.path.join("downloads", "youtube")


class YouTube_Downloader(Downloader):
    """Downloads YouTube videos as MP3 and retrieves metadata."""

    def __init__(self, debug: bool):
        self.debug = debug

    def download_mp3(self) -> str:
        """Downloads the video as an MP3 file."""
        return self._download_file(self._get_ydl_opts(audio_only=True), MP3_EXTENSION)

    def download_metadata(self) -> dict:
        """Downloads video metadata as a JSON file and returns its contents."""
        metadata_path = self._download_file(
            self._get_ydl_opts(metadata_only=True), METADATA_EXTENSION
        )

        try:
            with open(metadata_path, "r", encoding="utf8") as file:
                if self.debug:
                    logger.info("Successfully downloaded episode metadata.")
                return json.load(file)
        except Exception as e:
            logger.error(f"Failed to read metadata file: {e}")
            return {}

    def download_episode(
        self, source_url: str, episode_name: str | None
    ) -> Tuple[str, str, str]:
        """Downloads both the MP3 file and metadata, then logs key details."""
        self.source_url = self._extract_video_url(source_url)
        self.video_id = self._extract_video_id()

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

    def _extract_video_url(self, source_url) -> str:
        """Extracts video URL from a source URL."""
        return source_url.split("&")[0]

    def _extract_video_id(self) -> str:
        """Extracts video ID from a source URL."""
        return self.source_url.split("=")[-1]

    def _download_file(self, ydl_opts: dict, extension: str) -> str:
        """Handles downloading the requested file type."""
        output_path = os.path.join(
            os.getcwd(), OUTPUT_DIR, self.video_id, f"{self.video_id}{extension}"
        )

        if os.path.exists(output_path):
            if self.debug:
                logger.info("File already exists.")
            return output_path

        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([self.source_url])
            except Exception as e:
                logger.error(f"Failed to download {extension}: {e}")
                raise

        if self.debug:
            logger.info("Successfully downloaded episode.")

        return output_path

    def _get_ydl_opts(
        self, audio_only: bool = False, metadata_only: bool = False
    ) -> dict:
        """Returns appropriate yt-dlp options based on request type."""
        opts = {
            "outtmpl": os.path.join(OUTPUT_DIR, "%(id)s", "%(id)s.%(ext)s"),
        }

        if audio_only:
            opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
            )

        if metadata_only:
            opts.update(
                {
                    "skip_download": True,
                    "writeinfojson": True,
                }
            )

        return opts
