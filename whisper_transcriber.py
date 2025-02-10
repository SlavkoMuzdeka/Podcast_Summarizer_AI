import os
import whisper
import logging

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

# Constants
YOUTUBE = 'youtube'
DOWNLOADS_DIR = "downloads"
YOUTUBE_BASE_URI = "https://www.youtube.com/watch?v="
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")


class WhisperTranscriber:
    def __init__(self):
        """
        Initializes the WhisperTranscriber with a specific model size.
        """
        self.model = whisper.load_model(WHISPER_MODEL)

    def transcribe(self, video_url: str, audio_path: str) -> str:
        self.video_id, self.source = self._extract_video_info(video_url)

        transcript_path = self._get_transcript_path()

        if os.path.exists(transcript_path):
            logger.info("Transcript already exists. Loading from file...")
            with open(transcript_path, "r", encoding="utf-8") as file:
                return file.read()
        
        logger.info("Starting transcription...")
        result = self.model.transcribe(audio_path)
        transcribed_text = result.get("text", "")

        self._save_transcript(transcript_path, transcribed_text)
        return transcribed_text

    def _extract_video_info(self, video_url: str) -> tuple[str, str]:
        """
        Extracts video ID and source from the given URL.
        """
        if YOUTUBE_BASE_URI in video_url:
            return video_url.split("=")[-1], YOUTUBE
        raise ValueError("Invalid YouTube URL. Please provide a valid video link.")

    def _get_transcript_path(self) -> str:
        """
        Constructs the path for storing the transcript.
        """
        return os.path.join(os.getcwd(), DOWNLOADS_DIR, self.source, self.video_id, f"{self.video_id}.txt")

    def _save_transcript(self, path: str, text: str):
        """
        Saves the transcribed text to a file.
        """
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
        logger.info(f"Transcript saved at: {path}")