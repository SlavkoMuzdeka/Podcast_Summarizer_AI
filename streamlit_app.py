import json
import logging
import streamlit as st

from dotenv import load_dotenv
from downloader import Downloader
from openai_summarizer import OpenAI_Summarizer
from youtube_downloader import YouTube_Downloader
from whisper_transcriber import Whisper_Transcriber
from rss_feed_downloader import RSS_Feed_Downloader
from utils.streamlit_utils import (
    is_valid_youtube_url,
    is_valid_rss_feed_url,
    is_rss_feed_episode_valid,
    show_succesfully_downloaded,
    show_succesfully_summarized,
    show_succesfully_transcribed,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Load application configuration
with open("config.json", "r") as f:
    config = json.load(f)


def summarize(
    summarizer: OpenAI_Summarizer,
    transcriber: Whisper_Transcriber,
    downloader: Downloader,
    source_url: str,
    episode_name: str | None,
):
    """
    Handles the entire process of downloading, transcribing, and summarizing a podcast episode.

    Parameters:
        summarizer (OpenAI_Summarizer): The summarizer instance for generating summaries.
        transcriber (Whisper_Transcriber): The transcriber instance for converting audio to text.
        downloader (Downloader): The downloader instance (YouTube or RSS-based).
        source_url (str): The URL of the podcast episode.
        episode_name (str | None): The name of the episode (applicable for RSS feeds only).
    """
    # User selects the level of detail for the summary
    detail_level = st.slider(
        "Select the level of detail:",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.05,
    )
    st.divider()

    mp3_file_path, transcribed_text = "", ""

    if st.button("Summarize"):
        # Step 1: Download the episode
        with st.spinner("Downloading episode...", show_time=True):
            mp3_file_path, mp3_file_title, video_id = downloader.download_episode(
                source_url, episode_name
            )
            show_succesfully_downloaded(mp3_file_title)

        # Step 2: Transcribe the episode
        if mp3_file_path:
            with st.spinner("Transcribing episode...", show_time=True):
                source = (
                    "youtube" if isinstance(downloader, YouTube_Downloader) else "rss"
                )
                transcribed_text = transcriber.transcribe(
                    source=source, audio_path=mp3_file_path, video_id=video_id
                )
                show_succesfully_transcribed()

        # Step 3: Summarize the transcription
        if transcribed_text:
            with st.spinner("Summarizing transcription...", show_time=True):
                summarized_text = summarizer.summarize(
                    transcribed_text, detail=detail_level
                )
                show_succesfully_summarized(summarized_text)


def main():
    """
    Main function that initializes Streamlit UI and handles user interactions.
    """
    st.title("Podcast Summarizer")

    # Initialize session state for necessary components
    if "youtube_downloader" not in st.session_state:
        st.session_state.youtube_downloader = YouTube_Downloader(config=config)

    if "rss_downloader" not in st.session_state:
        st.session_state.rss_downloader = RSS_Feed_Downloader(config=config)

    if "whisper_transcriber" not in st.session_state:
        st.session_state.whisper_transcriber = Whisper_Transcriber(config=config)

    if "openai_summarizer" not in st.session_state:
        st.session_state.openai_summarizer = OpenAI_Summarizer(config=config)

    # Retrieve instances from session state
    rss_downloader = st.session_state.rss_downloader
    openai_summarizer = st.session_state.openai_summarizer
    youtube_downloader = st.session_state.youtube_downloader
    whisper_transcriber = st.session_state.whisper_transcriber

    # User selects platform type
    choice = st.radio(
        "Select a platform:",
        ["YouTube", "Other Podcasts (Spotify, Apple Podcasts, Podcast Addict, ...)"],
    )

    if choice == "YouTube":
        # Handle YouTube input
        source_url = st.text_input("Enter YouTube Podcast Episode URL:", "")
        if source_url:
            if is_valid_youtube_url(source_url):
                summarize(
                    summarizer=openai_summarizer,
                    transcriber=whisper_transcriber,
                    downloader=youtube_downloader,
                    source_url=source_url,
                    episode_name=None,
                )
            else:
                st.error("Please enter a valid YouTube URL.")

    else:
        # Handle RSS feed input
        source_url = st.text_input("Enter Podcast RSS Feed URL:", "")
        if source_url:
            if is_valid_rss_feed_url(source_url):
                episode_name = st.text_input("Enter Episode Name:", "")
                if episode_name:
                    if is_rss_feed_episode_valid(source_url, episode_name):
                        summarize(
                            summarizer=openai_summarizer,
                            transcriber=whisper_transcriber,
                            downloader=rss_downloader,
                            source_url=source_url,
                            episode_name=episode_name,
                        )
                    else:
                        st.error("Episode not found. Please check the episode name.")
            else:
                st.error("Please enter a valid RSS Feed URL.")


if __name__ == "__main__":
    main()
