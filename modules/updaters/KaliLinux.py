from functools import cache
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from modules.exceptions import VersionNotFoundError
from modules.updaters.GenericUpdater import GenericUpdater
from modules.utils import parse_hash, sha256_hash_check

DOMAIN = "https://cdimage.kali.org"
DOWNLOAD_PAGE_URL = urljoin(DOMAIN, "current/")
FILE_NAME = "kali-linux-[[VER]]-[[EDITION]]-amd64.iso"


class KaliLinux(GenericUpdater):
    """
    A class representing an updater for Kali Linux.

    Attributes:
        valid_editions (list[str]): List of valid editions to use
        edition (str): Edition to download
        download_page (requests.Response): The HTTP response containing the download page HTML.
        soup_download_page (BeautifulSoup): The parsed HTML content of the download page.

    Note:
        This class inherits from the abstract base class GenericUpdater.
    """

    def __init__(self, folder_path: Path, edition: str) -> None:
        self.valid_editions = [
            "installer",
            "installer-netinst",
            "installer-purple",
            "live",
        ]
        self.edition = edition.lower()

        file_path = folder_path / FILE_NAME
        super().__init__(file_path)

        self.download_page = requests.get(DOWNLOAD_PAGE_URL)

        if self.download_page.status_code != 200:
            raise ConnectionError(
                f"Failed to fetch the download page from '{DOWNLOAD_PAGE_URL}'"
            )

        self.soup_download_page = BeautifulSoup(
            self.download_page.content, features="html.parser"
        )

    @cache
    def _get_download_link(self) -> str:
        return urljoin(
            DOWNLOAD_PAGE_URL,
            str(self._get_complete_normalized_file_path(absolute=False)),
        )

    def check_integrity(self) -> bool:
        sha256_url = urljoin(DOWNLOAD_PAGE_URL, "SHA256SUMS")

        sha256_sums = requests.get(sha256_url).text

        sha256_sum = parse_hash(
            sha256_sums,
            [str(self._get_complete_normalized_file_path(absolute=False))],
            0,
        )

        return sha256_hash_check(
            self._get_complete_normalized_file_path(absolute=True),
            sha256_sum,
        )

    @cache
    def _get_latest_version(self) -> list[str]:
        download_a_tags = self.soup_download_page.find_all("a", href=True)
        if not download_a_tags:
            raise VersionNotFoundError("We were not able to parse the download page")

        latest = next(
            href
            for a_tag in download_a_tags
            if str(
                self._get_normalized_file_path(
                    absolute=False,
                    version=None,
                    edition=self.edition if self.has_edition() else None,  # type: ignore
                    lang=self.lang if self.has_lang() else None,  # type: ignore
                )
            ).split("[[VER]]")[-1]
            in (href := a_tag.get("href"))
        )

        return self._str_to_version(latest.split("-")[2])
