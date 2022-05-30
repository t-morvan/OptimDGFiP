""""
Download data
"""

import os
import zipfile
from urllib.request import urlretrieve

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


def get_data() -> None:
    """
    Télécharge tous les fichiers nécessaires à l'étude
    """

    if not os.path.isdir("data"):
        os.mkdir("data")

    with open("../URLS.yaml", "r", encoding="utf-8") as file:
        links = yaml.safe_load(file)

    # download files and unzip them
    for link in links:
        name = link["filename"]
        download(link["url"], name)
        if name.endswith(".zip"):
            with zipfile.ZipFile(f"data/{name}", "r") as zip_ref:
                zip_ref.extractall(f"data/{name.replace('.zip','')}")


if __name__ == "__main__":
    get_data()
