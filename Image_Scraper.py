import requests
from bs4 import BeautifulSoup
import os

#Define a variable for the URL of the page from which to retreive the image
url = "https://qube.com.au/about/"

#Headers needed to mimic a browser request to avoid being blocked by the website's server
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

#Send a request to the URL
response = requests.get(url, headers=headers)
response.raise_for_status()

#Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

#Find the specific image tag by its attributes (found by going through the html source code)
image_tag = soup.find('img', {'class': 'extended-image nitro-lazy'})  # Search by class

#Find and download the image if the tag is found
if image_tag:
    image_src = image_tag.get('nitro-lazy-src')

    if image_src:
        image_response = requests.get(image_src, headers=headers)
        image_response.raise_for_status()

        #Save the image as a .png file
        image_name = "mia-train.png"
        with open(image_name, 'wb') as file:
            file.write(image_response.content)
        print(f"Image downloaded and saved as {image_name}")
    else:
        print("Image source not found in 'nitro-lazy-src' attribute.")
else:
    print("Specified image not found on the page.")