import os
import spotipy
import logging
import requests
import urllib.parse

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")


class Spotify_Downloader:
    def __init__(self):
        auth_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET
        )
        self.client = spotipy.Spotify(auth_manager=auth_manager)

    def download_episode(self, podcast_url):
        parsed_url = urllib.parse.urlparse(podcast_url)
        podcast_id = parsed_url.path.split("/")[-1]

        episode = self.client.episode(podcast_id, market="US")
        audio_url = episode["audio_preview_url"]
        response = requests.get(audio_url)
        filename = f"{podcast_id}.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"Episode downloaded: {filename}")
