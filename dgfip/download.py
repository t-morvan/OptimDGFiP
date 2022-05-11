import os
from urllib.request import urlopen, urlretrieve  

def download_url(url: str) -> None:
    """Download a file from a url and place it in root.
    Args:
        url (str): URL to download file from
        root (str): Directory to place downloaded file in
        filename (str, optional): Name to save the file under. If None, use the basename of the URL
    """

    root = f'{os.getcwd()}/data'
    os.makedirs(root, exist_ok=True)

     print("Downloading " + url + " to " + fpath)
     response = urlopen(url)
     filename = response.info().get_filename()  
     fpath = os.path.join(root, filename)
                       
     urlretrieve(url, fpath)
   

if __name__ == "__main__":
    download_url(
        "https://www.data.gouv.fr/fr/datasets/r/2b410993-9018-488c-8259-fe8cf9073a66"
    )
