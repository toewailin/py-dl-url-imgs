import os
import requests
from bs4 import BeautifulSoup

# Load the HTML file
file_path = "books.html"  # Update with the correct path
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse HTML
soup = BeautifulSoup(html_content, "html.parser")

# Dictionary to store book data
books_data = []

# Function to download images
def download_image(img_url, save_folder, img_name):
    if not img_url.startswith("http"):
        img_url = "https:" + img_url  # Fix missing schema
    response = requests.get(img_url, stream=True)
    if response.status_code == 200:
        os.makedirs(save_folder, exist_ok=True)
        img_path = os.path.join(save_folder, img_name)
        with open(img_path, "wb") as img_file:
            for chunk in response.iter_content(1024):
                img_file.write(chunk)
        return img_path
    return None

# Scrape book data
for book_section in soup.find_all("div", class_="book-info"):  # Adjust based on actual HTML structure
    title_tag = book_section.find("h2")
    img_tag = book_section.find("img")
    
    if title_tag and img_tag:
        title = title_tag.text.strip()
        img_url = img_tag["src"]
        category = book_section.find_previous("li").text.strip()  # Assuming books are under categories

        # Store book info
        book_info = {
            "title": title,
            "category": category,
            "image_url": img_url
        }
        books_data.append(book_info)

        # Download image
        img_ext = img_url.split(".")[-1]
        img_name = f"{title.replace(' ', '_')}.{img_ext}"
        download_image(img_url, f"books_info_images/{category}", img_name)

# Print extracted book data
for book in books_data[:10]:  # Show first 10 for verification
    print(book)
