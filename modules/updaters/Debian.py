import os

import requests
from bs4 import BeautifulSoup, Tag

from modules.exceptions import VersionNotFoundError
from modules.updaters.GenericUpdater import GenericUpdater
from modules.utils import parse_hash, sha256_hash_check

DOMAIN = "https://cdimage.debian.org"
DOWNLOAD_PAGE_URL = f"{DOMAIN}/debian-cd/current-live/amd64/iso-hybrid/"
FILE_NAME = "debian-live-[[VER]]-amd64-[[EDITION]].iso"


class Debian(GenericUpdater):
    """
    A class representing an updater for Debian Live (KDE).

    Attributes:
        valid_editions (list[str]): List of valid editions to use
        edition (str): Edition to download
        download_page (requests.Response): The HTTP response containing the download page HTML.
        soup_download_page (BeautifulSoup): The parsed HTML content of the download page.
        soup_index_list (Tag): The index list containing the downloadable files.

    Note:
        This class inherits from the abstract base class GenericUpdater.
    """

    def __init__(self, folder_path: str, edition: str) -> None:
        self.valid_editions = [
            "cinnamon",
            "gnome",
            "kde",
            "lxde",
            "lxqt",
            "mate",
            "standard",
            "xfce",
        ]

        self.edition = edition.lower()

        file_path = os.path.join(folder_path, FILE_NAME)
        super().__init__(file_path)

        # Make the parameter case insensitive, and find back the correct case using valid_editions

        self.download_page = requests.get(DOWNLOAD_PAGE_URL)

        if self.download_page.status_code != 200:
            raise ConnectionError(
                f"Failed to fetch the download page from '{DOWNLOAD_PAGE_URL}'"
            )

        self.soup_download_page = BeautifulSoup(
            self.download_page.content, features="html.parser"
        )

        self.soup_index_list: Tag = self.soup_download_page.find(
            "table", attrs={"id": "indexlist"}
        )  # type: ignore

        if not self.soup_index_list:
            raise ConnectionError(
                "We couldn't find the list of indexes containing the download URLs"
            )

    def _get_download_link(self) -> str:
        return (
            f"{DOWNLOAD_PAGE_URL}/{self._get_versioned_latest_file_name(edition=True)}"
        )

    def check_integrity(self) -> bool:
        sha256_url = f"{DOWNLOAD_PAGE_URL}/SHA256SUMS"

        sha256_sums = requests.get(sha256_url).text

        sha256_sum = parse_hash(
            sha256_sums, [self._get_versioned_latest_file_name(edition=True)], 0
        )

        return sha256_hash_check(
            self._get_versioned_latest_file_name(absolute=True, edition=True),
            sha256_sum,
        )

    def _get_latest_version(self) -> list[str]:
        download_a_tags = self.soup_index_list.find_all("a", href=True)
        if not download_a_tags:
            raise VersionNotFoundError("We were not able to parse the download page")

        latest = next(
            href
            for a_tag in download_a_tags
            if self._get_editioned_file_name().split("[[VER]]")[-1]
            in (href := a_tag.get("href"))
        )

        return self._str_to_version(latest.split("-")[2])
