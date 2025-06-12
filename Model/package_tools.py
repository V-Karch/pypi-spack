import os


class PackageTools:
    def __init__(self, tar_title: str):
        self.tar_title = tar_title

    def find_packaging_files(self) -> list[str]:
        packaging_files: list[str] = [
            "pyproject.toml",
            "setup.py",
            "pkg-info",
            "requirements.txt",
            "requirements",
            "setup.cfg",
        ]

        found_packaging_files: list[str] = []

        for file in os.listdir(self.tar_title.replace(".tar.gz", "")):
            if file.lower() in packaging_files:
                found_packaging_files.append(file)

        if "requirements" in found_packaging_files:
            found_packaging_files.remove("requirements")
            for file in os.listdir(
                f"{self.tar_title.replace('.tar.gz', '')}/requirements"
            ):
                found_packaging_files.append(file)

        return found_packaging_files
