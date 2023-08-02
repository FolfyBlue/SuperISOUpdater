import os

import requests
from bs4 import BeautifulSoup, Tag

from modules.exceptions import VersionNotFoundError
from modules.updaters.GenericUpdater import GenericUpdater
from modules.utils import sha256_hash_check, windows_consumer_download

DOMAIN = "https://www.microsoft.com"
DOWNLOAD_PAGE_URL = f"{DOMAIN}/en-us/software-download/windows11"
FILE_NAME = "Win11_[[VER]]_EnglishInternational_x64v2.iso"


class Windows11(GenericUpdater):
    """
    A class representing an updater for Windows11.

    Attributes:
        download_page (requests.Response): The HTTP response containing the download page HTML.
        soup_download_page (BeautifulSoup): The parsed HTML content of the download page.
        soup_main_content (Tag): The main contents of the page.

    Note:
        This class inherits from the abstract base class GenericUpdater.
    """

    def __init__(self, folder_path: str) -> None:
        file_path = os.path.join(folder_path, FILE_NAME)
        super().__init__(file_path)
        self.version_splitter = "H"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "referer": "folfy.blue",
        }

        self.download_page = requests.get(DOWNLOAD_PAGE_URL, headers=self.headers)

        if self.download_page.status_code != 200:
            raise ConnectionError(
                f"Failed to fetch the download page from '{DOWNLOAD_PAGE_URL}'"
            )

        self.soup_download_page = BeautifulSoup(
            self.download_page.content, features="html.parser"
        )

        self.soup_main_content: Tag = self.soup_download_page.find(
            "main", attrs={"id": "mainContent"}
        )  # type: ignore

        if not self.soup_main_content:
            raise ConnectionError("Failed to fetch the main content from the webpage")

        self.hash: str | None = None

    def _get_download_link(self) -> str:
        download_link, self.hash = windows_consumer_download(windows_version="11")
        return download_link

    def check_integrity(self) -> bool:
        if not self.hash:
            return False

        return sha256_hash_check(
            self._get_versioned_latest_file_name(absolute=True),
            self.hash,
        )

    def _get_latest_version(self) -> list[str]:
        header: Tag | None = self.soup_main_content.find("header")  # type: ignore
        if not header:
            raise VersionNotFoundError(
                "Could not find header containing version information"
            )

        return [
            version_number.strip()
            for version_number in header.getText()
            .split("Version")[1]
            .replace(")", "")
            .split("H")
        ]
