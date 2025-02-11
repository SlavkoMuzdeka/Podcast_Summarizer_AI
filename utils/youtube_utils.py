import os
import logging

logger = logging.getLogger(__name__)


def extract_video_url(source_url) -> str:
    """
    Extracts the base video URL from a YouTube source URL.

    Some YouTube URLs contain additional parameters (e.g., timestamps, playlists).
    This function ensures only the core video URL is returned.

    Args:
        source_url (str): The full YouTube video URL.

    Returns:
        str: The cleaned video URL without extra parameters.
    """
    return source_url.split("&")[0]


def extract_video_id(source_url) -> str:
    """
    Extracts the video ID from a YouTube URL.

    The video ID is the unique identifier assigned to each YouTube video.
    It is typically found after "v=" in the URL.

    Args:
        source_url (str): The YouTube video URL.

    Returns:
        str: The extracted video ID.
    """
    return source_url.split("=")[-1]


def get_ydl_opts(output_dir: str, audio_only: bool = False) -> dict:
    """
    Generates configuration options for yt-dlp based on download requirements.

    This function prepares options for yt-dlp, specifying output format,
    download type (audio or metadata), and necessary post-processing steps.

    Args:
        output_dir (str): The directory where the downloaded files should be saved.
        audio_only (bool, optional): Whether to download only audio. Defaults to False.

    Returns:
        dict: The yt-dlp configuration options.
    """
    opts = {
        "outtmpl": os.path.join(output_dir, "%(id)s", "%(id)s.%(ext)s"),
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
        return opts
    opts.update(
        {
            "skip_download": True,
            "writeinfojson": True,
        }
    )
    return opts
