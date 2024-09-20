import os
import requests
import re
import datetime
import time
import json

# Load configuration from JSON file
def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"The configuration file '{config_file}' does not exist. Please refer to the README for setup instructions: https://github.com/Dave-Swagten/Medal.tv-Bulk-Downloader?tab=readme-ov-file#%EF%B8%8F-configuration")
        
        exit(1)
    except json.JSONDecodeError:
        print("Error parsing the configuration file. Ensure it is valid JSON format.")
        exit(1)

# Parse cookies from the configuration
def parse_cookies(cookies_list):
    cookies_dict = {}
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']
    return cookies_dict

# Load configuration
config_file = 'config.json'
config = load_config(config_file)
COOKIES = parse_cookies(config['cookies'])
USER_ID = config['user_id']

def download_mp4(content_url, filename, download_folder):
    try:
        filepath = os.path.join(download_folder, filename)
        
        # Check if the file already exists in the download folder
        if os.path.exists(filepath):
            print(f"File already exists: {filepath}")
            return
        
        # Sleep for 1 second before making the request (to prevent rate limit errors)
        time.sleep(1)
        
        response = requests.get(content_url, cookies=COOKIES)
        
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded clip {filename}")
        else:
            print(f"Failed to download {content_url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {content_url}: {e}")

# Function to sanitize filename by removing invalid characters (otherwise files will end up not being mp4 files)
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def convert_timestamp_to_date(timestamp_ms):
    """Convert milliseconds timestamp to a human-readable date string."""
    timestamp_s = timestamp_ms / 1000
    date_time = datetime.datetime.fromtimestamp(timestamp_s)
    return date_time.strftime("%Y-%m-%d_%H-%M-%S")

def fetch_data(user_id, offset, sort_direction):
    try:
        url = f"https://medal.tv/api/content?userId={user_id}&limit=100&offset={offset}&sortBy=publishedAt&sortDirection={sort_direction}"
        response = requests.get(url, cookies=COOKIES)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data from API with offset {offset}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data from API with offset {offset}: {e}")
        return None

def main():
    offset = 0
    download_folder = "downloads"
    processed_files = set()

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # User input for sorting order
    while True:
        print("Choose sorting order for the clips:")
        print("1. Descending (newest first)")
        print("2. Ascending (oldest first)")
        choice = input("Enter 1 or 2: ")
        
        if choice == '1':
            sort_direction = 'DESC'
            break
        elif choice == '2':
            sort_direction = 'ASC'
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    # User input for number of clips to download
    while True:
        try:
            max_clips = int(input("Enter the number of clips to download (0 for all): "))
            if max_clips < 0:
                print("Please enter a non-negative number.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    total_downloaded = 0
    
    while True:
        print(f"Fetching data with offset {offset}...")
        data = fetch_data(USER_ID, offset, sort_direction)
        
        if not data:
            print("No data returned or error occurred. Exiting.")
            break
        
        if not isinstance(data, list):
            print(f"Unexpected data format. Expected list but got {type(data)}.")
            break
        
        video_count = 0
        batch_start_time = time.time()

        for item in data:
            if max_clips > 0 and total_downloaded >= max_clips:
                print(f"Reached the specified number of clips ({max_clips}). Stopping download.")
                return

            if 'contentUrl' in item and 'publishedAt' in item:
                try:
                    content_title = item.get('contentTitle', 'Untitled')
                    content_url = item['contentUrl']
                    published_at = item['publishedAt']
                    
                    # Convert the publishedAt timestamp to a date string
                    date_str = convert_timestamp_to_date(published_at)
                    
                    # Format filename with title and date
                    sanitized_title = sanitize_filename(content_title)
                    filename = f"{date_str}_{sanitized_title}.mp4"
                    
                    # Check for duplicates
                    if filename not in processed_files:
                        download_mp4(content_url, filename, download_folder)
                        processed_files.add(filename)
                        video_count += 1
                        total_downloaded += 1
                    else:
                        print(f"Duplicate file detected, skipping {filename}.")
                    
                except Exception as e:
                    print(f"Error processing item: {item}. Exception: {e}")
            else:
                print(f"Skipping item: {item.get('contentTitle', 'Untitled')}. Missing required fields.")

        elapsed_time = time.time() - batch_start_time
        delay = max(0, 1 - elapsed_time)  # Ensuring that we do not sleep for negative time (because time travel is not supported)
        print(f"Processed {video_count} videos in this batch. Sleeping for {delay:.2f} seconds.")
        time.sleep(delay)
        
        # Update offset for next batch. This is the number of videos processed so far
        offset += video_count
        print(f"\nCompleted batch. New offset is {offset}.")
        print(f"Total videos processed: {total_downloaded}")
        print(f"Elapsed time for this batch: {elapsed_time:.2f} seconds.\n")

        if max_clips > 0 and total_downloaded >= max_clips:
            print(f"Reached the specified number of clips ({max_clips}). Stopping download.")
            break

if __name__ == "__main__":
    main()
