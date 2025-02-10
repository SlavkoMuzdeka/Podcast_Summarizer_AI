import logging

from openai_summarizer import OpenAI_Summarizer
from youtube_downloader import YouTube_Downloader
from whisper_transcriber import WhisperTranscriber

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    # youtube_url = "https://www.youtube.com/watch?v=ms-5iTsCroI"
    youtube_url = "https://www.youtube.com/watch?v=NhHnIlRlGts"

    yt = YouTube_Downloader()
    mp3_path = yt.download_episode(youtube_url)

    whisper = WhisperTranscriber()
    transcribed_text = whisper.transcribe(youtube_url, mp3_path)

    openai_summarizer = OpenAI_Summarizer()
    summary, api_cost = openai_summarizer.summarize(transcribed_text)
    logger.info(f"↪ 💵 GPT3 cost: ${api_cost:.2f}.")
    logger.info(f"\nSummary: \n{summary}")

    with open("summary.txt", "w", encoding="utf-8") as file:
        file.write(summary)


if __name__ == "__main__":
    main()
