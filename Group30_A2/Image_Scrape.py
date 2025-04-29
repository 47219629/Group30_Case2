import requests
from bs4 import BeautifulSoup
import os

#Define the URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Qube_Holdings"

#Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

#Send a request to the website
response = requests.get(url, headers=headers)
response.raise_for_status()  # Check for request errors

#Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

#Find the specific image tag
image_tag = soup.find('img', {'class': 'mw-file-element'})

if image_tag:
    image_src = image_tag.get('src')

    if image_src:
        image_url = "https:" + image_src

        #Request to download the image
        image_response = requests.get(image_url, headers=headers)
        image_response.raise_for_status()

        #Save the image
        image_name = "Scraped_Image.png"
        with open(image_name, 'wb') as file:
            file.write(image_response.content)
        print(f"Image downloaded and saved as {image_name}")
    else:
        print("Image source not found in the 'src' attribute.")
else:
    print("Specified image not found on the page.")