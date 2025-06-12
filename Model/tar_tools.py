import os
import shutil
import hashlib
import tarfile
import requests


class TarTools:
    """
    A utility class for downloading, extracting, cleaning up, and verifying .tar.gz files.

    Attributes:
        url (str): The URL of the .tar.gz file to manage.
        tar_title (str): The filename extracted from the URL.
    """

    def __init__(self, url: str):
        """
        Initializes a TarTools object with a given URL.

        Args:
            url (str): The URL pointing to the .tar.gz file.
        """

        self.url = url
        self.tar_title = self.url.split("/")[-1]

    def check_tar_downloaded(self):
        """
        Checks if the .tar.gz file exists in the current directory.

        Raises:
            FileNotFoundError: If the file is not found in the current directory.
        """

        if not self.tar_title in os.listdir():
            raise FileNotFoundError(
                f"./{self.tar_title} could not be found, please first download it using TarTools().download_tar()"
            )

    def download_tar(self) -> bool:
        """
        Downloads the .tar.gz file from the specified URL and saves it locally.

        Returns:
            bool: True if download was successful, False otherwise.
        """

        response: requests.Response = requests.get(self.url)

        try:
            with open(self.tar_title, "wb") as f:
                f.write(response.content)

            return True
        except Exception:
            return False

    def untar_tar(self) -> bool:
        """
        Extracts the downloaded .tar.gz file into the current directory.

        Returns:
            bool: True if extraction was successful, False otherwise.

        Raises:
            FileNotFoundError: If the file does not exist locally.
        """

        self.check_tar_downloaded()

        try:
            tar = tarfile.open(self.tar_title, "r:gz")
            tar.extractall()
            tar.close()
            return True
        except Exception:
            return False

    def cleanup_tar(self) -> bool:
        """
        Deletes the downloaded .tar.gz file and its extracted contents.

        Returns:
            bool: True if cleanup was successful, False otherwise.

        Raises:
            FileNotFoundError: If the file does not exist locally.
        """

        self.check_tar_downloaded()

        try:
            os.remove(self.tar_title)
            shutil.rmtree(self.tar_title.replace(".tar.gz", ""))
            return True
        except Exception:
            return False

    def get_tar_checksum(self) -> str:
        """
        Computes the SHA-256 checksum of the downloaded .tar.gz file.

        Returns:
            str: The SHA-256 checksum as a hexadecimal string.

        Raises:
            FileNotFoundError: If the file does not exist locally.
        """

        self.check_tar_downloaded()

        with open(self.tar_title, "rb") as f:
            data = f.read()

        return hashlib.sha256(data).hexdigest()
