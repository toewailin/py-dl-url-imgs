import os
import requests

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

# Create a temporary directory to store the images
temp_dir = "temp_images"
os.makedirs(temp_dir, exist_ok=True)

# Base URL components
base_url = "https://win99.org/images/C_images/all_bg/iframe_101/bet/"
image_name = "onbet_{}_nobet.png"
options = [
    "big", "small", "banker", "player", "tie", "dragon", "tiger", "roulette", 
    "blackjack", "poker", "baccarat", "craps", "keno", "slot", "sicbo"
]

# Loop through the range of styles, onbet_ values, and options to download each image
for style_number in range(2, 11):  # Adjust the range as needed
    for option in options:
        url = f"{base_url}style_{style_number}/{image_name.format(option)}"
        save_path = os.path.join(temp_dir, f"style_{style_number}_onbet_{option}_nobet.png")
        download_image(url, save_path)

print("All image downloads attempted.")
