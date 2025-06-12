from Model.tar_tools import TarTools


def main() -> None:
    tar_tools = TarTools(
        "https://files.pythonhosted.org/packages/38/10/a7f63e086c1e1c12e290c98363c748ef5ddd6313fde739d2aeccd5ed0cd4/deepspeed-0.17.1.tar.gz"
    )

    print(tar_tools.download_tar())
    print(tar_tools.untar_tar())
    print(tar_tools.cleanup_tar())


if __name__ == "__main__":
    main()
