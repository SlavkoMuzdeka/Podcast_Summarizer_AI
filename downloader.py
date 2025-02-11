from typing import Tuple


class Downloader:
    def download_episode(
        self, source_url: str, episode_name: str | None
    ) -> Tuple[str, str, str]:
        pass
