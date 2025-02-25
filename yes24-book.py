import os
import requests
from bs4 import BeautifulSoup

# Base URL for the image
image_base_url = "https://image.yes24.com/goods/"

# Directory to save downloaded images
output_directory = "downloaded_images"

# URL of the page you want to scrape
url = "https://www.yes24.com/Product/Category/Display/001001019"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Send GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all book items
items = soup.find_all('li', class_='item')

# Loop through each item to get the book title (gd_name) and ID from the link
for item in items:
    try:
        # Extract the book title (gd_name)
        book_title = item.find('a', class_='gd_name').text.strip()

        # Extract the item ID from the URL
        item_url = item.find('a', class_='lnk_img')['href']
        item_id = item_url.split('/')[-1]

        # Construct the image URL
        image_url = f"{image_base_url}{item_id}/L"
        
        # Generate the filename with the format: book_title_item_id.jpg
        filename = f"{book_title}_{item_id}.jpg"
        filepath = os.path.join(output_directory, filename)

        # Send GET request to fetch the image
        img_response = requests.get(image_url, stream=True)
        img_response.raise_for_status()

        # Check if the image is valid
        if "image" in img_response.headers.get("Content-Type", ""):
            # Save the image to the file
            with open(filepath, "wb") as f:
                for chunk in img_response.iter_content(1024):
                    f.write(chunk)

            print(f"Downloaded: {filename}")
        else:
            print(f"No image found for ID: {item_id}")
    
    except Exception as e:
        print(f"Failed to download image for ID {item_id}: {e}")

print(f"Images downloaded to {output_directory}")
