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

    def parse_packaging_file(self, filetype: str):
        filetype = filetype.lower()

        if filetype == "pkg-info":
            self.parse_pkg_info()
        elif filetype == "setup.py":
            self.parse_setup_py()
        elif filetype == "pyproject.toml":
            self.parse_pyproject_toml()
        elif filetype == "requirements.txt":
            self.parse_requirements_txt()
        elif filetype == "setup.cfg":
            self.parse_setup_cfg()
        elif "requirements" in filetype:
            self.parse_requirements_other()
        else:
            raise ValueError(
                f"{filetype} is an invalid option for PackageTools.parse_packaging_file(self, filetype: str)"
            )

    def parse_pkg_info(self):
        pkg_info: str = self.tar_title.replace(".tar.gz", "") + "/PKG-INFO"
        with open(pkg_info, "r") as f:
            data = [line.strip() for line in f.readlines()]

        print(data)

    def parse_setup_py(self):
        pass

    def parse_pyproject_toml(self):
        pass

    def parse_setup_cfg(self):
        pass

    def parse_requirements_txt(self):
        pass

    def parse_requirements_other(self):
        pass
