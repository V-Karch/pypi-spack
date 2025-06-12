import os
from Model.requirements_parser import RequirementParser


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
                found_packaging_files.append("requirements/" + file)

        return found_packaging_files

    def parse_packaging_file(self, filename: str) -> list[str]:
        filename = filename.lower()

        if filename == "pkg-info":
            return self.parse_pkg_info(filename)
        elif filename == "setup.py":
            return self.parse_setup_py(filename)
        elif filename == "pyproject.toml":
            return self.parse_pyproject_toml(filename)
        elif filename == "requirements.txt":
            return self.parse_requirements_txt(filename)
        elif filename == "setup.cfg":
            return self.parse_setup_cfg(filename)
        elif "requirements" in filename:
            return self.parse_requirements_other(filename)
        else:
            raise ValueError(
                f"{filename} is an invalid option for PackageTools.parse_packaging_file(self, filename: str)"
            )

    def parse_pkg_info(self, filename: str):
        print(f"\nParsing {filename}...\n")
        return []

    def parse_setup_py(self, filename: str):
        print(f"\nParsing {filename}...\n")
        return []

    def parse_pyproject_toml(self, filename: str):
        print(f"\nParsing {filename}...\n")
        return []

    def parse_setup_cfg(self, filename: str):
        print(f"\nParsing {filename}...\n")
        return []

    def parse_requirements_txt(self, filename: str):
        print(f"\nParsing {filename}...\n")

        requirement_parser = RequirementParser(
            self.tar_title.replace(".tar.gz", "") + "/" + filename
        )

        return requirement_parser.parse()

    def parse_requirements_other(self, filename: str):
        print(f"\nParsing {filename}...\n")

        requirement_parser = RequirementParser(
            self.tar_title.replace(".tar.gz", "") + "/" + filename
        )

        return requirement_parser.parse()
