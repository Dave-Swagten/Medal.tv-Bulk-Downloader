import datetime
import re
from config import CONFIG

def update_cache(content_id):
    file_path = CONFIG['CACHE_FILE']
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