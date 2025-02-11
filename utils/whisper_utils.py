import os
import logging

DOWNLOADS_DIR = "downloads"  # Directory where transcripts are stored
TRANSCRIPTION_EXTENSION = ".txt"  # File extension for saved transcripts

logger = logging.getLogger(__name__)


def get_transcript_path(source, video_id) -> str:
    """
    Constructs the path for storing the transcript.

    Args:
        source: The source of the audio (e.g., "youtube").
        video_id: The unique identifier of the audio/video file.
        model (whisper.Whisper): Loaded Whisper model for transcription.

    Returns:
        str: Full path where the transcript should be stored.
    """
    return os.path.join(
        os.getcwd(),
        DOWNLOADS_DIR,
        source,
        video_id,
        f"{video_id}{TRANSCRIPTION_EXTENSION}",
    )


def save_transcript(debug: bool, path: str, text: str):
    """
    Saves the transcribed text to a file.

    Args:
        debug: If True, logs the save location.
        path: Path where the transcript should be saved.
        text: The transcribed text to write to the file.
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)

    if debug:
        logger.info(f"Transcript saved at: {path}")
