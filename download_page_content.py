from bs4 import BeautifulSoup
import requests
import re

with open('htb_links.txt', 'r') as file:
    urls = file.read().splitlines()

for url in urls:
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    #soup = BeautifulSoup(html_content, 'html.parser')

    rows = soup.find_all('tr')

    ####################
    ##Difficulty rating#
    ####################

    # Iterating through the rows and extracting the text
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 2:
            # Check if the first cell contains a <picture> element
            if cells[0].find('picture') is None:
                key = cells[0].get_text(strip=True)
                if key not in ["Rated Difficulty", "Radar Graph", "Retire Date", "Creator"]:
                    value = cells[1].get_text(strip=True)
                    print(f"{key} : {value}")


    #################
    #####Nmap Text###
    #################

    pre_tag = soup.find('pre', class_='highlight')

    # If the pre_tag is found, process it
    if pre_tag:
        # Get the text content of the <pre> tag
        pre_text = pre_tag.get_text()

        # Define the start and end patterns
        start_pattern = re.compile(r'Nmap scan report for.*')
        end_pattern = re.compile(r'Nmap done.*')

        # Search for the start and end patterns
        start_match = start_pattern.search(pre_text)
        end_match = end_pattern.search(pre_text)

        # Extract the text between the start and end matches
        if start_match and end_match:
            start_index = start_match.end()
            end_index = end_match.start()
            nmap_output = pre_text[start_index:end_index].strip()
            print(nmap_output)
        else:
            print("Patterns not found in the text.")
    else:
        print("No <pre> tag with the specified class found.")


    print('##############################################################')

    #################
    #####Paragraphs between Headers with "shell-as" in ID###
    #################

    # Find all headers with "shell-as" in their ID
    # Dictionary to store content by header
    content_by_header = {}

    # Variable to keep track of the current header
    current_header = None

    # Define the ID patterns to match
    patterns = ['recon', 'shell-as-', 'auth-as-', 'rce-as-']

    # Function to check if an ID matches any of the patterns
    def id_matches(id):
        return any(id.startswith(pattern) for pattern in patterns)

    # Iterate over all elements in the soup
    for element in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        # Check if the element is a header and its ID matches any of the patterns
        if element.name in ['h2', 'h3', 'h4', 'h5', 'h6'] and id_matches(element.get('id', '')):
            current_header = element.get_text()
            content_by_header[current_header] = []
        # If the element is a paragraph and we have a current header
        elif element.name == 'p' and current_header:
            content_by_header[current_header].append(element.get_text())

    # Print the extracted contents
    for header, paragraphs in content_by_header.items():
        print(f"Header: {header}")
        for paragraph in paragraphs:
            if "Click for full size image" not in paragraph:
                print(f"{paragraph}")
        print("\n")