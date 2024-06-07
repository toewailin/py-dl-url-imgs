import os
import requests
import zipfile

# Function to download an image and save it to a specified directory
def download_image(url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {save_path}")
        else:
            print(f"Failed to download (status code {response.status_code}): {url}")
    except Exception as e:
        print(f"An error occurred while downloading {url}: {str(e)}")

# Function to zip the directory
def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
    print(f"Zipped folder: {zip_path}")

# Create a temporary directory to store the images
temp_dir = "temp_images"
os.makedirs(temp_dir, exist_ok=True)

# Base URL components
# "https://win99.org/images/C_images/all_bg/iframe_101/bet/style_2/roomstyle_1/information_bg.png"
base_url = "https://win99.org/images/C_images/all_bg/iframe_101/bet/"
image_name = "information_bg.png"

# Loop through the range of styles and roomstyles to download each image
for style_number in range(1, 9):  # Adjust the range as needed
    for roomstyle_number in range(1, 13):  # Adjust the range as needed
        url = f"{base_url}style_{style_number}/roomstyle_{roomstyle_number}/{image_name}"
        save_path = os.path.join(temp_dir, f"style_{style_number}_roomstyle_{roomstyle_number}.png")
        download_image(url, save_path)

# Zip the temp_images directory
zip_path = "temp_images.zip"
zip_directory(temp_dir, zip_path)

print("All image downloads attempted and folder zipped.")
