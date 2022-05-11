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
   
def main() -> None:
     with open('datalinks.txt', 'r', encoding='utf-8') as file:
        for line in file:
            link = file.readline()
            download_url(link)
     
    
    
if __name__ == "__main__":
    main()
   
      
