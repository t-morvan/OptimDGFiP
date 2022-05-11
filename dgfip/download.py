import os
from urllib.request import urlopen, urlretrieve  
import zipfile

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
   
def main() -> None:
    # downlload all files
     with open('datalinks.txt', 'r', encoding='utf-8') as file:
        for line in file:
            link = file.readline()
            download_url(link)
     
    # unzip them
    for file in os.listdir('data'):
        if file.endswith('.zip'):  
            with zipfile.ZipFile(f'data/{file}, 'r') as zip_ref:
                zip_ref.extractall('data')

if __name__ == "__main__":
    main()
   
      
