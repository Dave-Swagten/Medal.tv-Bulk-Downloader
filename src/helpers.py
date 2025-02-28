import datetime
import re
from config import CONFIG

def update_cache(content_id):
    file_path = CONFIG['CACHE_FILE']
    if file_path != '':
        with open(file_path, 'a') as file:
            file.write(content_id + "\n")

def format_filename(filename, published_at, category):
    # Convert the publishedAt timestamp to a date string
    date_str = convert_timestamp_to_date(published_at)
    comp_date_str = convert_timestamp_to_compact_date(published_at)
    comp_time_str = convert_timestamp_to_compact_time(published_at)
    title_format = CONFIG['TITLE_FORMAT']
    # sanitize filename by removing invalid characters (otherwise files will end up not being mp4 files)
    sanitized_title = re.sub(r'[<>:"/\\|?*]', '', filename)
    # could be some funky categories out there
    sanitized_category = re.sub(r'[<>:"/\\|?*]', '', category)
    # Format filename with title and date
    return f"{title_format.format(
            category=sanitized_category,
            compact_date=comp_date_str,
            compact_time=comp_time_str,
            date=date_str,
            title=sanitized_title
    )}.mp4"

def convert_timestamp_to_date(timestamp_ms):
    """Convert milliseconds timestamp to a human-readable date string."""
    timestamp_s = timestamp_ms / 1000
    date_time = datetime.datetime.fromtimestamp(timestamp_s)
    return date_time.strftime("%Y-%m-%d_%H-%M-%S")

def convert_timestamp_to_compact_date(timestamp_ms):
    """Convert milliseconds timestamp to a compact human-readable date string."""
    timestamp_s = timestamp_ms / 1000
    date_time = datetime.datetime.fromtimestamp(timestamp_s)
    return date_time.strftime("%y%m%d")

def convert_timestamp_to_compact_time(timestamp_ms):
    """Convert milliseconds timestamp to a human-readable time string."""
    timestamp_s = timestamp_ms / 1000
    date_time = datetime.datetime.fromtimestamp(timestamp_s)
    return date_time.strftime("%H%M%S")