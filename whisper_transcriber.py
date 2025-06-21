import os
import math
import whisper
import logging
import streamlit as st

from openai import OpenAI
from pydub import AudioSegment

logger = logging.getLogger(__name__)

MAX_FILE_SIZE_MB = 25
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


class Whisper_Transcriber:
    """
    A class for transcribing audio files using OpenAI's Whisper model.

    Attributes:
        config (dict): Configuration dictionary containing settings like model type and verbose mode.
        verbose (bool): Flag to enable or disable verbosing logs.
        model (whisper.Whisper): Loaded Whisper model for transcription.
    """

    def __init__(self, config: dict):
        """
        Initializes the WhisperTranscriber with a specific model size.

        Args:
            config (dict): Configuration settings, including 'WHISPER_MODEL' and 'VERBOSE'.
        """
        self.config = config
        self.verbose = config.get("verbose", False)
        self.model = whisper.load_model(config.get("model", "base"))
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    def transcribe_api(self, audio_path: str, video_id: str) -> str:
        base_dir = os.path.join(
            os.getcwd(),
            self.config.get("downloads_dir", "downloads"),
            video_id,
        )
        transcript_path = os.path.join(
            base_dir,
            f"{video_id}{self.config.get('transcription_extension', '.txt')}",
        )

        if self.verbose and os.path.exists(transcript_path):
            logger.info("Transcription already exists.")
            with open(transcript_path, "r", encoding="utf-8") as file:
                return file.read()

        if self.verbose:
            logger.info("Starting transcription...")

        transcribed_text = ""

        if os.path.getsize(audio_path) <= MAX_FILE_SIZE_BYTES:
            # File is within size limit, process directly
            with open(audio_path, "rb") as audio_file:
                result = self.client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, response_format="json"
                )
                transcribed_text = result.text
        else:
            if self.verbose:
                size_mb = os.path.getsize(audio_path) / (1024 * 1024)
                logger.info(
                    f"Audio file exceeds 25MB ({size_mb:.2f} MB), splitting into chunks..."
                )

            audio = AudioSegment.from_file(audio_path)
            duration_ms = len(audio)
            estimated_size_per_ms = os.path.getsize(audio_path) / duration_ms
            chunk_duration_ms = int(MAX_FILE_SIZE_BYTES / estimated_size_per_ms)

            chunks = math.ceil(duration_ms / chunk_duration_ms)

            os.makedirs(base_dir, exist_ok=True)

            for i in range(chunks):
                start_ms = i * chunk_duration_ms
                end_ms = min((i + 1) * chunk_duration_ms, duration_ms)
                chunk = audio[start_ms:end_ms]

                chunk_path = os.path.join(
                    base_dir, f"{video_id}_{i+1}{self.config.get('mp3_ext', '.mp3')}"
                )

                chunk.export(chunk_path, format="mp3")

                with open(chunk_path, "rb") as audio_file:
                    result = self.client.audio.transcriptions.create(
                        model="whisper-1", file=audio_file, response_format="json"
                    )
                    transcribed_text += result.text

                if self.verbose:
                    logger.info(f"Processed chunk {i + 1} of {chunks}")

                os.remove(chunk_path)

        if self.verbose:
            with open(transcript_path, "w", encoding="utf-8") as file:
                file.write(transcribed_text)
            logger.info(f"Transcript saved at: {transcript_path}")

        return transcribed_text

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
        if self.verbose and os.path.exists(transcript_path):
            logger.info("Transcription already exists.")
            with open(transcript_path, "r", encoding="utf-8") as file:
                return file.read()

        if self.verbose:
            logger.info("Starting transcription...")

        # Perform transcription
        result = self.model.transcribe(audio_path)

        if self.verbose:
            logger.info("Transcription finished.")

        transcribed_text = result.get("text", "")

        if self.verbose:
            with open(transcript_path, "w", encoding="utf-8") as file:
                file.write(transcribed_text)
                logger.info(f"Transcript saved at: {transcript_path}")

        return transcribed_text
