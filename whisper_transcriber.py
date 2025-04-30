import os
import whisper
import logging

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
        self.debug = config.get("debug", False)
        self.model = whisper.load_model(config.get("model", "base"))

    def transcribe(self, audio_path: str, video_id: str) -> str:
        """
        Transcribes an audio file into text using the Whisper model.

        Args:
            audio_path (str): The file path of the audio to be transcribed.
            video_id (str): Unique identifier for the audio/video.

        Returns:
            str: The transcribed text.
        """
        transcript_path = os.path.join(
            os.getcwd(),
            self.config.get("downloads_dir", "downloads"),
            video_id,
            f"{video_id}{self.config.get('transcription_extension', '.txt')}",
        )

        # Check if a transcription already exists to avoid re-processing
        if self.debug and os.path.exists(transcript_path):
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

        if self.debug:
            with open(transcript_path, "w", encoding="utf-8") as file:
                file.write(transcribed_text)
                logger.info(f"Transcript saved at: {transcript_path}")

        return transcribed_text
