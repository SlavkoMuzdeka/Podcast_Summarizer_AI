import json
import logging

from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from openai_summarizer import OpenAI_Summarizer
from youtube_downloader import YouTube_Downloader
from whisper_transcriber import Whisper_Transcriber
from rss_feed_downloader import RSS_Feed_Downloader

# Load env & config
load_dotenv(override=True)
with open("config.json") as f:
    config = json.load(f)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)

yt_downloader = YouTube_Downloader(config=config["youtube"])
rss_downloader = RSS_Feed_Downloader(config=config)
transcriber = Whisper_Transcriber(config=config["whisper"])
summarizer = OpenAI_Summarizer(config=config["openai"])

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])


@app.route("/api/summarize", methods=["POST"])
@cross_origin()
def summarize_endpoint():
    """
    Expects JSON with:
      - source_url: str
      - episode_name: str | null
      - detail_level: float (0.0–1.0)
      - platform: "youtube" or "rss"
    Returns JSON with:
      - success: bool
      - summary: str (if success)
      - error: str (if not)
    """
    data = request.get_json()
    source_url = data.get("source_url")
    episode_name = data.get("episode_name")
    detail_level = data.get("detail_level", 0.0)
    platform = data.get("platform")

    # pick downloader
    if platform == "youtube":
        downloader = yt_downloader
    else:
        downloader = rss_downloader

    try:
        # 1) Download
        mp3_path, metadata = downloader.download_episode(source_url, episode_name)
        logger.info(f"Downloaded {metadata.get('title', '')}")

        # 2) Transcribe
        text = transcriber.transcribe(
            audio_path=mp3_path, video_id=metadata.get("id", "")
        )
        logger.info("Transcription complete")

        # 3) Summarize
        summary = summarizer.summarize(text, detail=detail_level)
        logger.info("Summarization complete")

        return (
            jsonify(
                {
                    "success": True,
                    "title": metadata.get("title", ""),
                    "summary": summary,
                    "thumbnail": metadata.get("thumbnail", ""),
                    "channel": metadata.get("channel", ""),
                    "duration_string": metadata.get("duration_string", ""),
                    "release_date": metadata.get("release_date", ""),
                }
            ),
            200,
        )

    except Exception as e:
        logger.exception("Error in /summarize")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run()
