import os
import requests
from bs4 import BeautifulSoup

# Base URL for the image
product_image_base_url = "https://image.yes24.com/goods/"
event_image_base_url = "https://image.yes24.com/"

# Directory to save downloaded images
output_directory = "downloaded_images"
os.makedirs(output_directory, exist_ok=True)

# URL of the page you want to scrape for events/categories
url = "https://www.yes24.com/Product/Category/Display/001001019"  # Adjust as needed for event/category pages

# Function to download a product image
def download_product_image(item_id):
    try:
        image_url = f"{product_image_base_url}{item_id}/L"
        filename = f"product_{item_id}_L.jpg"
        filepath = os.path.join(output_directory, filename)

        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # Check if the image is valid (e.g., server returns an image)
        if "image" in response.headers.get("Content-Type", ""):
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print(f"Downloaded: {filename}")
        else:
            print(f"No image found for product ID: {item_id}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download product image for ID {item_id}: {e}")

# Function to download event/category image
def download_event_image(image_url, filename):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        if "image" in response.headers.get("Content-Type", ""):
            filepath = os.path.join(output_directory, filename)
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print(f"Downloaded: {filename}")
        else:
            print(f"Not a valid image for {image_url}")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image from {image_url}: {e}")

# Scrape the page to get event/category image URLs
def scrape_event_images(page_url):
    try:
        # Send GET request to the category/event page
        response = requests.get(page_url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all img tags in the page and filter URLs that belong to images
        img_tags = soup.find_all('img')

        event_image_urls = []

        for img_tag in img_tags:
            img_url = img_tag.get('data-original') or img_tag.get('src')
            if img_url and img_url.startswith("https://image.yes24.com/"):
                event_image_urls.append(img_url)

        return event_image_urls

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch event images from {page_url}: {e}")
        return []

# Download images for all event/category URLs scraped
event_image_urls = scrape_event_images(url)

for event_image_url in event_image_urls:
    filename = event_image_url.split("/")[-1]  # Extract filename from URL
    download_event_image(event_image_url, filename)

# Download product images for a range of item IDs
start_id = 126590468  # Start ID for product images
end_id = 126590475    # End ID for product images (adjust as needed)

for item_id in range(start_id, end_id + 1):
    download_product_image(item_id)

print(f"Images downloaded to {output_directory}")
