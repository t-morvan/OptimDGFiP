import os
import zipfile
from urllib.request import urlopen, urlretrieve

import yaml


def download(url: str, name: str) -> None:
    """Download a file from a url and place it in root.
    Args:
        url (str): URL to download file from
        root (str): Directory to place downloaded file in
        filename (str, optional): Name to save the file under. If None, use the basename of the URL
    """

    print(f"Downloading {url}")

    urlretrieve(url, f"data/{name}")


def main() -> None:

    if not os.path.isdir("data"):
        os.mkdir("data")

    with open("LINKS.yaml", "r", encoding="utf-8") as file:
        links = yaml.safe_load(file)

    # download files and unzip them
    for name, link in links.items():
        download(link, name)
        if name.endswith(".zip"):
            with zipfile.ZipFile(f"data/{name}", "r") as zip_ref:
                zip_ref.extractall(f"data/{name.replace('.zip','')}")


if __name__ == "__main__":
    main()
