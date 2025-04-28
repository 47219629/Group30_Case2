import requests
from bs4 import BeautifulSoup
import json

# URL of the Qube Holdings "About" page
url = "https://qube.com.au/about/"

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# Send a GET request to the website
response = requests.get(url, headers=headers)
response.raise_for_status()  # Check for request errors

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find the JSON-LD script tag containing the logo information
json_ld_tag = soup.find('script', type='application/ld+json', class_='rank-math-schema')

if json_ld_tag:
    # Parse the JSON-LD content
    json_data = json.loads(json_ld_tag.string)

    # Extract the logo URL from the JSON-LD data
    logo_url = None
    if isinstance(json_data, dict) and "@graph" in json_data:
        for item in json_data["@graph"]:
            if item.get("@type") == "Organization" and "logo" in item:
                logo_url = item["logo"].get("contentUrl")
                break

    if logo_url:
        # Download the logo image
        logo_response = requests.get(logo_url, headers=headers)
        logo_response.raise_for_status()

        # Save the logo as a .svg file
        logo_name = "logo-qube.svg"
        with open(logo_name, 'wb') as file:
            file.write(logo_response.content)
        print(f"Logo downloaded and saved as {logo_name}")
    else:
        print("Logo URL not found in JSON-LD data.")
else:
    print("JSON-LD data not found on the page.")