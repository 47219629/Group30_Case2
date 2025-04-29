import requests
from bs4 import BeautifulSoup
import json
import cairosvg  # Library to convert SVG to PNG

# Define a variable for the URL of the page from which to retrieve the image
url = "https://qube.com.au/about/"

# Headers needed to mimic a browser request to avoid being blocked by the website's server
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# Send a request to the URL
response = requests.get(url, headers=headers)
response.raise_for_status()  # Check for request errors

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find the script tag containing the logo information and extract the data
json_ld_tag = soup.find('script', type='application/ld+json', class_='rank-math-schema')

if json_ld_tag:
    json_data = json.loads(json_ld_tag.string)

    logo_url = None
    if isinstance(json_data, dict) and "@graph" in json_data:
        for item in json_data["@graph"]:
            if item.get("@type") == "Organization" and "logo" in item:
                logo_url = item["logo"].get("contentUrl")
                break

    if logo_url:
        # Download the logo as SVG
        logo_response = requests.get(logo_url, headers=headers)
        logo_response.raise_for_status()

        # Save the SVG file temporarily
        svg_name = "logo-qube.svg"
        with open(svg_name, 'wb') as file:
            file.write(logo_response.content)

        # Convert the SVG to PNG
        png_name = "Scraped_Image.png"
        cairosvg.svg2png(url=svg_name, write_to=png_name)
        print(f"Logo downloaded and converted to {png_name}")
    else:
        print("Logo URL not found in data.")
else:
    print("Data not found on the page.")
