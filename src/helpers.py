import datetime
import re
from config import CONFIG

def update_cache(content_id):
    file_path = CONFIG['CACHE_FILE']
    if file_path != '':
        with open(file_path, 'a') as file:
            file.write(content_id + "\n")

def format_filename(filename, published_at):
    # Convert the publishedAt timestamp to a date string
    date_str = convert_timestamp_to_date(published_at)
    title_format = CONFIG['TITLE_FORMAT']
    # sanitize filename by removing invalid characters (otherwise files will end up not being mp4 files)
    sanitized_title = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Format filename with title and date
    return f"{title_format.format(date=date_str, title=sanitized_title)}.mp4"

def convert_timestamp_to_date(timestamp_ms):
    """Convert milliseconds timestamp to a human-readable date string."""
    timestamp_s = timestamp_ms / 1000
    date_time = datetime.datetime.fromtimestamp(timestamp_s)
    return date_time.strftime("%Y-%m-%d_%H-%M-%S")