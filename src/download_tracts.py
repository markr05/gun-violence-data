import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_census_tracts():
    base_url = "https://www2.census.gov/geo/tiger/TIGER2017/TRACT/"
    output_dir = "../data/census_tracts"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # getting the page content
    print("Connecting to Census Bureau servers...")
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to access page. Status code: {response.status_code}")
        return

    # finding all zip files
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for a in soup.find_all('a'):
        # Check if the tag has an 'href' AND if that 'href' ends with '.zip'
        if a.has_attr('href') and a['href'].endswith('.zip'):
            links.append(a['href'])

    print(f"Found {len(links)} state tract files to download.")

    # download every file
    for link in links:
        file_url = urljoin(base_url, link)
        file_path = os.path.join(output_dir, link)

        if os.path.exists(file_path):
            print(f"Skipping {link} (already exists).")
            continue

        print(f"Downloading {link}...", end="\r")
        r = requests.get(file_url, stream=True)
        
        if r.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        else:
            print(f"Failed to download {link}")

    print("\n" + "="*30)
    print("All downloads finished!")

if __name__ == "__main__":
    download_census_tracts()