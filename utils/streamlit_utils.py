import re


def is_valid_youtube_url(url: str) -> bool:
    """
    Returns True if the provided URL is exactly in the format:
      https://www.youtube.com/watch?v=VIDEO_ID&
    where VIDEO_ID is exactly 11 characters (letters, numbers, '-' or '_'),
    and the URL ends with an ampersand.
    """
    pattern = r"^https://www\.youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})(?:&.*)?$"
    return re.match(pattern, url) is not None
