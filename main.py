from Model.tar_tools import TarTools
from Model.package_tools import PackageTools


def main() -> None:
    tar_tools = TarTools(
        "https://files.pythonhosted.org/packages/38/10/a7f63e086c1e1c12e290c98363c748ef5ddd6313fde739d2aeccd5ed0cd4/deepspeed-0.17.1.tar.gz"
    )
    package_tools = PackageTools(tar_tools.tar_title)

    tar_tools.download_tar()
    tar_tools.untar_tar()

    found_packaging_files = package_tools.find_packaging_files()

    for packaging_file in found_packaging_files:
        print(f"\n{packaging_file}\n")
        print(package_tools.parse_packaging_file(packaging_file))

    tar_tools.cleanup_tar()


if __name__ == "__main__":
    main()
