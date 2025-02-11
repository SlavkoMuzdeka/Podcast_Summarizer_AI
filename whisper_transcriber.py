import os
import whisper
import logging

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

# Constants
YOUTUBE = "youtube"
ENCODING_TYPE = "utf-8"
DOWNLOADS_DIR = "downloads"
TRANSCRIPTION_EXTENSION = ".txt"
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
YOUTUBE_BASE_URI = "https://www.youtube.com/watch?v="


class Whisper_Transcriber:
    def __init__(self, debug: bool):
        """
        Initializes the WhisperTranscriber with a specific model size.
        """
        self.model = whisper.load_model(WHISPER_MODEL)
        self.debug = debug

    def transcribe(self, source: str, audio_path: str, video_id: str) -> str:
        self.source, self.video_id = source, video_id
        transcript_path = self._get_transcript_path()

        if os.path.exists(transcript_path):
            if self.debug:
                logger.info("Transcription already exists.")

            with open(transcript_path, "r", encoding=ENCODING_TYPE) as file:
                return file.read()

        if self.debug:
            logger.info("Starting transcription...")

        result = self.model.transcribe(audio_path)

        if self.debug:
            logger.info("Transcription finished.")

        transcribed_text = result.get("text", "")

        self._save_transcript(transcript_path, transcribed_text)
        return transcribed_text

    def _get_transcript_path(self) -> str:
        """
        Constructs the path for storing the transcript.
        """
        return os.path.join(
            os.getcwd(),
            DOWNLOADS_DIR,
            self.source,
            self.video_id,
            f"{self.video_id}{TRANSCRIPTION_EXTENSION}",
        )

    def _save_transcript(self, path: str, text: str):
        """
        Saves the transcribed text to a file.
        """
        with open(path, "w", encoding=ENCODING_TYPE) as file:
            file.write(text)

        if self.debug:
            logger.info(f"Transcript saved at: {path}")
