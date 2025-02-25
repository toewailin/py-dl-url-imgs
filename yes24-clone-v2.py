import os
import time
import requests
import urllib.robotparser
import logging
from random import randint, choice
from itertools import cycle

# Configure logging
logging.basicConfig(
    filename="image_downloader.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Base URL for the image
image_base_url = "https://secimage.yes24.com/goods/"

# Directory to save downloaded images
output_directory = "downloaded_images"

# Range of possible item IDs
start_id = 10724
end_id = 999999999

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Pool of user-agents to rotate
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1",
]

# Optional proxy pool (uncomment and configure if needed)
# proxies = [
#     "http://154.202.123.76:80",
#     "http://198.23.226.22:3128",
# ]
# proxy_cycle = cycle(proxies)

# Check robots.txt compliance
def is_allowed_by_robots(url):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url("https://secimage.yes24.com/robots.txt")
    try:
        rp.read()
        return rp.can_fetch(choice(user_agents), url)
    except Exception as e:
        logging.warning(f"Failed to read robots.txt: {e}. Assuming allowed.")
        return True

# Download image function
def download_image(item_id, session, proxy=None):
    try:
        image_url = f"{image_base_url}{item_id}/L"
        filename = f"{item_id}_L.jpg"
        filepath = os.path.join(output_directory, filename)

        if os.path.exists(filepath):
            logging.info(f"Skipped (already exists): {filename}")
            return True  # Count existing files as "downloaded"

        if not is_allowed_by_robots(image_url):
            logging.warning(f"robots.txt disallows crawling: {image_url}")
            return False

        # Rotate user-agent for each request
        headers = {"User-Agent": choice(user_agents)}
        proxy_dict = {"http": proxy, "https": proxy} if proxy else {}

        # Send GET request
        response = session.get(image_url, headers=headers, proxies=proxy_dict, stream=True, timeout=10)
        response.raise_for_status()

        # Check for rate limiting (HTTP 429)
        if response.status_code == 429:
            logging.warning(f"Rate limit hit for ID {item_id}. Waiting 60 seconds...")
            time.sleep(60)
            return False

        if "image" in response.headers.get("Content-Type", ""):
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            logging.info(f"Downloaded: {filename}")
            return True
        else:
            logging.info(f"No image found for ID: {item_id}")
            return False

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download image for ID {item_id}: {e}")
        return False

# Main execution
def main():
    download_count = 0  # Initialize counter for successful downloads

    with requests.Session() as session:
        # Uncomment the following line if using proxies
        # proxy_iterator = proxy_cycle
        for item_id in range(start_id, end_id + 1):
            # Use proxy if enabled, otherwise None
            current_proxy = None  # Replace with next(proxy_iterator) if using proxies
            success = download_image(item_id, session, current_proxy)

            # Increment counter if download was successful
            if success:
                download_count += 1

            # Print current book ID and download count to console
            print(f"Processing book ID: {item_id} | Total downloaded: {download_count}")

            # Random delay between 1-5 seconds to avoid detection
            delay = randint(1, 5)
            logging.info(f"Waiting {delay} seconds before next request...")
            time.sleep(delay)

    logging.info(f"Images downloaded to {output_directory}")
    print(f"Final number of items downloaded: {download_count}")

if __name__ == "__main__":
    try:
        logging.info("Starting image downloader...")
        print("Starting image downloader...")
        main()
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
        print("Script interrupted by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
    finally:
        logging.info("Script execution completed.")
        print("Script execution completed.")