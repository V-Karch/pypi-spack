from Model.tar_tools import TarTools
from Model.package_tools import PackageTools


def main() -> None:
    tar_tools = TarTools(
        "https://files.pythonhosted.org/packages/bb/50/e0f9f8a6de373f6431928bcb4b1499d34708994326b85cea4f791da4f39b/rgbprint-4.0.2.tar.gz"
    )
    package_tools = PackageTools(tar_tools.tar_title)

    tar_tools.download_tar()
    tar_tools.untar_tar()

    found_packaging_files = package_tools.find_packaging_files()

    for packaging_file in found_packaging_files:
        package_tools.parse_packaging_file(packaging_file)

    tar_tools.cleanup_tar()


if __name__ == "__main__":
    main()
