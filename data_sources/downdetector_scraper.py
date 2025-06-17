import requests
from bs4 import BeautifulSoup

def fetch_downdetector():
    url = 'https://downdetector.com/'
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get list of current major outages
    outages = []
    outage_blocks = soup.find_all('li', class_='entry-title')

    for block in outage_blocks:
        service = block.text.strip()
        link = block.find('a')['href']
        outages.append({'service': service, 'link': f'https://downdetector.com{link}'})

    return outages
