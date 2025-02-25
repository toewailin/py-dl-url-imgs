import os
import requests

# Base URL for the image
image_base_url = "https://secimage.yes24.com/goods/"

# Directory to save downloaded images
output_directory = "downloaded_images"

# Range of possible item IDs (adjust range as needed)
start_id = 10002  # Example start ID
end_id = 999999999    # Example end ID

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Define a browser user-agent to avoid being blocked by the server
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Loop through possible item IDs
for item_id in range(start_id, end_id + 1):
    try:
        # Construct the image URL
        image_url = f"{image_base_url}{item_id}/L"
        # Extract the filename
        filename = f"{item_id}_L.jpg"
        filepath = os.path.join(output_directory, filename)

        # Send GET request with headers including the user-agent
        response = requests.get(image_url, headers=headers, stream=True)
        response.raise_for_status()

        # Check if the image is valid (e.g., server returns an image)
        if "image" in response.headers.get("Content-Type", ""):
            # Save the image to file
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print(f"Downloaded: {filename}")
        else:
            print(f"No image found for ID: {item_id}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download image for ID {item_id}: {e}")

print(f"Images downloaded to {output_directory}")
