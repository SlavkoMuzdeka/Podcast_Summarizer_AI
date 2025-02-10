# from spotify_downloader import Spotify_Downloader
from rss_downloader import RSSDownloader


def main():
    # spotify = Spotify_Downloader()
    # spotify.download_episode(
    #     "https://open.spotify.com/episode/5eG4T1AdkBseCU3QdpDiKP?si=8I1d2teoSIC_WE34Qo4NnQ"
    # )
    # https://open.spotify.com/episode/5eG4T1AdkBseCU3QdpDiKP?si=8I1d2teoSIC_WE34Qo4NnQ
    # https://open.spotify.com/episode/5eG4T1AdkBseCU3QdpDiKP?si=8I1d2teoSIC_WE34Qo4NnQ&nd=1&dlsi=0183a75afd1b4f55
    rss_downloader = RSSDownloader()
    rss_downloader.download_episode(
        "https://feeds.megaphone.fm/empire",
        "Why DeepSeek Disrupted Markets & How Tokens Are The New GTM | Roundup",
    )


if __name__ == "__main__":
    main()
