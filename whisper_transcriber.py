import os
import whisper
import logging

from utils.whisper_utils import get_transcript_path, save_transcript

logger = logging.getLogger(__name__)


class Whisper_Transcriber:
    """
    A class for transcribing audio files using OpenAI's Whisper model.

    Attributes:
        config (dict): Configuration dictionary containing settings like model type and debug mode.
        debug (bool): Flag to enable or disable debugging logs.
        model (whisper.Whisper): Loaded Whisper model for transcription.
    """

    def __init__(self, config: dict):
        """
        Initializes the WhisperTranscriber with a specific model size.

        Args:
            config (dict): Configuration settings, including 'WHISPER_MODEL' and 'DEBUG'.
        """
        self.config = config
        self.debug = self.config.get("DEBUG", False)
        self.model = whisper.load_model(self.config.get("WHISPER_MODEL", "base"))

    def transcribe(self, source: str, audio_path: str, video_id: str) -> str:
        """
        Transcribes an audio file into text using the Whisper model.

        Args:
            source (str): The source platform or category of the audio.
            audio_path (str): The file path of the audio to be transcribed.
            video_id (str): Unique identifier for the audio/video.

        Returns:
            str: The transcribed text.
        """
        self.source, self.video_id = source, video_id
        transcript_path = get_transcript_path(self.source, self.video_id)

        # Check if a transcription already exists to avoid re-processing
        if os.path.exists(transcript_path):
            if self.debug:
                logger.info("Transcription already exists.")
            with open(transcript_path, "r", encoding="utf-8") as file:
                return file.read()

        if self.debug:
            logger.info("Starting transcription...")

        # Perform transcription
        result = self.model.transcribe(audio_path)

        if self.debug:
            logger.info("Transcription finished.")

        transcribed_text = result.get("text", "")

        # Save the transcription to a file
        save_transcript(self.debug, transcript_path, transcribed_text)
        return transcribed_text
