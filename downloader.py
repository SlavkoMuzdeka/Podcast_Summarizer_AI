from typing import Tuple


class Downloader:
    def downloade_episode(
        self, source_url: str, episode_name: str | None, debug: bool = False
    ) -> Tuple[str, str, str]:
        pass
