from backend.base.definitions import DownloadSource, DownloadState
from backend.base.helpers import Session
from backend.implementations.download_general import Download


class BaseReaderDownload(Download):
    def __init__(self, download_link: str, filename_body: str, source: DownloadSource, custom_name: bool = True) -> None:
        self._ssn = Session()
        self.id = None
        self.state : DownloadState = DownloadState.QUEUED_STATE
        self.progress: float = 0.0
        self.speed: float = 0.0
        self.size: int = 0
        self.download_link = download_link
        self.source = source

    def _get_image_list(self) -> list[str]:
        """Fetches the list of images to download"""
        return []

    def run(self) -> None:
        self.state = DownloadState.DOWNLOADING_STATE
        for image in self._get_image_list():
            req = self._ssn.get(image)
            if req.raise_for_status():
                self.state = DownloadState.FAILED_STATE
                break
            if self.state in (DownloadState.CANCELED_STATE,
                                    DownloadState.SHUTDOWN_STATE):
                break
