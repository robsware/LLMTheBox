import requests
import re
from bs4 import BeautifulSoup

def scrape_links_and_save():
    # Hardcoded URL of the webpage to scrape
    url = 'https://0xdf.gitlab.io'  # Replace with the actual URL
    # Hardcoded output file path
    output_file = 'data/htb_links.txt'

    # Send a GET request to the webpage
    response = requests.get(url)
    links_list = []
    complete_links_list = []

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all 'a' tags with the class 'post-link'
        links = soup.find_all('a', class_='post-link')
        
        # Extract the href attribute of each link
        for link in links:
            href = link.get('href')
            if href and re.search(r'/\d{4}/\d{2}/\d{2}/htb-[^/]+\.html$', href):
                links_list.append(href)
    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

    for link in links_list:
        link = url + link
        complete_links_list.append(link)

    with open(output_file, 'w') as f:
        for link in complete_links_list:
            if "sherlock" not in link.lower():  # Use .lower() to make the check case-insensitive
                f.write(f"{link}\n")

#scrape_links_and_save()
