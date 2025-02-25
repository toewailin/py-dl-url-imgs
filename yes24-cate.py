import os
import requests

# Base URL for product images
product_image_base_url = "https://image.yes24.com/goods/"

# Base URL for category/event images
event_image_base_url = "https://image.yes24.com/"

# Directory to save downloaded images
output_directory = "downloaded_images"
os.makedirs(output_directory, exist_ok=True)

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

# Example list of event/category images (use known paths or URLs)
event_image_urls = [
    "https://image.yes24.com/images/00_Event/2024/1218Bjorn/bn_720x360.jpg",
    "https://image.yes24.com/images/13_EventWorld/250286_01.jpg",
    # Add more event/category URLs here
]

# Download product images for a range of item IDs
start_id = 126590468  # Start ID for product images
end_id = 126590475    # End ID for product images (adjust as needed)

for item_id in range(start_id, end_id + 1):
    download_product_image(item_id)

# Download event/category images from the list
for event_image_url in event_image_urls:
    filename = event_image_url.split("/")[-1]  # Extract the file name from the URL
    download_event_image(event_image_url, filename)

print(f"Images downloaded to {output_directory}")
