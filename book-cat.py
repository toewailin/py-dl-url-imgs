import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Load the HTML file
html_file = "books.html"

# Read the HTML content
with open(html_file, "r", encoding="utf-8") as file:
    content = file.read()

# Parse the HTML
soup = BeautifulSoup(content, "html.parser")

# Base URL of the website
BASE_URL = "https://www.yes24.com"

# Function to sanitize category names (remove invalid characters)
def sanitize_filename(name):
    return name.replace("/", "_").replace("\\", "_").replace(":", "_") \
               .replace("*", "_").replace("?", "_").replace('"', "_") \
               .replace("<", "_").replace(">", "_").replace("|", "_").strip()

# Find categories
categories = {}
for category in soup.find_all("li"):
    category_link = category.find("a")
    if category_link and "href" in category_link.attrs:
        category_name = sanitize_filename(category_link.text.strip())  # Sanitize name
        categories[category_name] = set()  # Use a set to avoid duplicate URLs

# Find images and associate with categories
for category, images in categories.items():
    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url:
            # Fix relative URLs (starting with `//`)
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            elif img_url.startswith("/"):
                img_url = urljoin(BASE_URL, img_url)

            # Skip blank images or empty URLs
            if "blank.gif" in img_url or img_url.strip() == "":
                continue

            images.add(img_url)  # Add to set (avoids duplicates)

# Download images and save into category folders
download_dir = "books_cat_images"
os.makedirs(download_dir, exist_ok=True)

for category, img_urls in categories.items():
    category_dir = os.path.join(download_dir, category)
    os.makedirs(category_dir, exist_ok=True)

    for img_url in img_urls:
        # Extract filename from the URL path
        parsed_url = urlparse(img_url)
        filename = os.path.basename(parsed_url.path)  # Extract filename from URL path

        # Ensure valid file extension
        valid_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        img_ext = os.path.splitext(filename)[-1].lower()

        if img_ext not in valid_extensions:
            img_ext = ".jpg"  # Default to .jpg if no valid extension found

        img_path = os.path.join(category_dir, filename)  # Keep original filename

        # Skip download if the file already exists
        if os.path.exists(img_path):
            print(f"Skipped (Already Exists) {img_path}")
            continue

        try:
            response = requests.get(img_url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(img_path, "wb") as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                print(f"Downloaded {img_url} -> {img_path}")
            else:
                print(f"Failed to download {img_url}, Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {img_url}: {e}")

print("Download completed!")
