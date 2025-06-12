import os
import shutil
import hashlib
import tarfile
import requests


class TarTools:
    def __init__(self, url: str):
        self.url = url
        self.tar_title = self.url.split("/")[-1]

    def check_tar_downloaded(self):
        if not self.tar_title in os.listdir():
            raise FileNotFoundError(
                f"./{self.tar_title} could not be found, please first download it using TarTools().download_tar()"
            )

    def download_tar(self) -> bool:
        response: requests.Response = requests.get(self.url)

        try:
            with open(self.tar_title, "wb") as f:
                f.write(response.content)

            return True
        except Exception:
            return False

    def untar_tar(self) -> bool:
        self.check_tar_downloaded()

        try:
            tar = tarfile.open(self.tar_title, "r:gz")
            tar.extractall()
            tar.close()
            return True
        except Exception:
            return False

    def cleanup_tar(self) -> bool:
        self.check_tar_downloaded()

        try:
            os.remove(self.tar_title)
            shutil.rmtree(self.tar_title.replace(".tar.gz", ""))
            return True
        except Exception:
            return False

    def get_tar_checksum(self) -> str:

        with open(self.tar_title, "rb") as f:
            data = f.read()

        return hashlib.sha256(data).hexdigest()
