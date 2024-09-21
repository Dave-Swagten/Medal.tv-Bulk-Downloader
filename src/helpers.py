import json
import datetime
import re

# Load configuration from JSON file
def load_config():
    config_file = 'config.json'
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"The configuration file '{config_file}' does not exist. Please refer to the README for setup instructions: https://github.com/Dave-Swagten/Medal.tv-Bulk-Downloader?tab=readme-ov-file#%EF%B8%8F-configuration")
        
        exit(1)
    except json.JSONDecodeError:
        print("Error parsing the configuration file. Ensure it is valid JSON format.")
        exit(1)

# Load cache file
def load_cache(file_path):
    if file_path != '':
        try:
            with open(file_path, 'r') as file:
                return set(file.read().splitlines())
        except FileNotFoundError:
            print(f"Cache file not found: {file_path}. Creating a new one.")
            open(file_path, 'w').close()  # Create an empty file
    return set()  # Return an empty set if no file path is provided or if the file is empty

def update_cache(content_id, file_path):
    if file_path != '':
        with open(file_path, 'a') as file:
            file.write(content_id + "\n")

# Parse cookies from the configuration
def parse_cookies(cookies_list):
    cookies_dict = {}
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']
    return cookies_dict


# Function to sanitize filename by removing invalid characters (otherwise files will end up not being mp4 files)
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def convert_timestamp_to_date(timestamp_ms):
    """Convert milliseconds timestamp to a human-readable date string."""
    timestamp_s = timestamp_ms / 1000
    date_time = datetime.datetime.fromtimestamp(timestamp_s)
    return date_time.strftime("%Y-%m-%d_%H-%M-%S")