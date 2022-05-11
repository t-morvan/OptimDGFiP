import os
import urllib.request


def download_url(url: str) -> None:
    """Download a file from a url and place it in root.
    Args:
        url (str): URL to download file from
        root (str): Directory to place downloaded file in
        filename (str, optional): Name to save the file under. If None, use the basename of the URL
    """

    root = f'{os.getcwd()}/data"
    filename = os.path.basename(url)
    fpath = os.path.join(root, filename)

    os.makedirs(root, exist_ok=True)

    try:
        print("Downloading " + url + " to " + fpath)
        urllib.request.urlretrieve(url, fpath)
    except (urllib.error.URLError, IOError) as e:
        if url[:5] == "https":
            url = url.replace("https:", "http:")
            print(
                "Failed download. Trying https -> http instead."
                " Downloading " + url + " to " + fpath
            )
            urllib.request.urlretrieve(url, fpath)


if __name__ == "__main__":
    download_url(
        "https://www.data.gouv.fr/fr/datasets/r/2b410993-9018-488c-8259-fe8cf9073a66"
    )
