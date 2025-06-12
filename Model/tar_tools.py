import os
import shutil
import tarfile
import requests


class TarTools:
    def __init__(self, url: str):
        self.url = url
        self.tar_title = self.url.split("/")[-1]

    def download_tar(self) -> bool:
        response: requests.Response = requests.get(self.url)

        try:
            with open(self.tar_title, "wb") as f:
                f.write(response.content)

            return True
        except Exception:
            return False

    def untar_tar(self) -> bool:
        try:
            tar = tarfile.open(self.tar_title, "r:gz")
            tar.extractall()
            tar.close()
            return True
        except Exception:
            return False

    def cleanup_tar(self) -> bool:
        try:
            os.remove(self.tar_title)
            shutil.rmtree(self.tar_title.replace(".tar.gz", ""))
            return True
        except Exception:
            return False
