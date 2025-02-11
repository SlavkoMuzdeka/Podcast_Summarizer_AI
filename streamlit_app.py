import os
import logging
import streamlit as st

from dotenv import load_dotenv
from utils import streamlit_utils
from rss_downloader import RSS_Downloader
from openai_summarizer import OpenAI_Summarizer
from youtube_downloader import YouTube_Downloader
from whisper_transcriber import Whisper_Transcriber

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)

DEBUG = os.getenv("DEBUG", False)
print(f"DEBUG is {DEBUG}")


# TODO Check if `source_url` is valid when entering path (JUST FOR RSS FEED URL)
# TODO Specify that before running the app, the machine should have installed `ffmpeg` package in order to download it


def main():
    st.title("Podcast Summarizer")

    if "youtube_downloader" not in st.session_state:
        st.session_state.youtube_downloader = YouTube_Downloader(debug=DEBUG)

    if "rss_downloader" not in st.session_state:
        st.session_state.rss_downloader = RSS_Downloader(debug=DEBUG)

    if "whisper_transcriber" not in st.session_state:
        st.session_state.whisper_transcriber = Whisper_Transcriber(debug=DEBUG)

    if "openai_summarizer" not in st.session_state:
        st.session_state.openai_summarizer = OpenAI_Summarizer()

    rss_downloader = st.session_state.rss_downloader
    openai_summarizer = st.session_state.openai_summarizer
    youtube_downloader = st.session_state.youtube_downloader
    whisper_transcriber = st.session_state.whisper_transcriber

    # Choice selection
    choice = st.radio(
        "Select a platform:",
        ["YouTube", "Other Podcasts (Spotify, Apple Podcasts, Podcast Addict, ...)"],
    )

    mp3_file_path, source = "", ""

    if choice == "YouTube":
        source_url = st.text_input("Enter YouTube Podcast Episode URL:", "")
        st.write("------------")
        if source_url:
            if streamlit_utils.is_valid_youtube_url(source_url):
                with st.spinner("Downloading episode..."):
                    mp3_file_path, mp3_file_title, video_id = (
                        youtube_downloader.download_episode(source_url, None)
                    )
                    source = "youtube"
                    st.subheader("✅ Downloaded")
                    st.write("Episode name:")
                    st.write(mp3_file_title)
            else:
                st.error("Please enter a valid YouTube URL.")

    else:
        source_url = st.text_input("Enter Podcast RSS Feed URL:", "")
        if source_url:
            downloader = rss_downloader
            episode_name = st.text_input("Enter Episode Name:", "")

    if mp3_file_path:
        with st.spinner("Transcribing episode..."):
            transcribed_text = whisper_transcriber.transcribe(
                source=source, audio_path=mp3_file_path, video_id=video_id
            )
            st.subheader("✅ Transcribed")
            st.write("Transcribed text is:")
            st.write(transcribed_text)

        with st.spinner("Summarizing transcription..."):
            summarized_text, _ = openai_summarizer.summarize(transcribed_text)
            st.subheader("✅ Summarized")
            st.write("Summarized text is:")
            st.write(summarized_text)


if __name__ == "__main__":
    main()
