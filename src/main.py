import time
from config import parse_config
from helpers import convert_timestamp_to_date, sanitize_filename, update_cache
from requestHelper import download_mp4, fetch_data

CONFIG = parse_config()

if __name__ == "__main__":
    offset = 0
    total_downloaded = 0
    processed_files = set()

    download_folder =  CONFIG['DOWNLOAD_FOLDER']
    sort_direction = CONFIG['SORT_DIRECTION']
    max_clips = CONFIG['MAX_CLIPS']
    cookies = CONFIG['COOKIES']
    user_id = CONFIG['USER_ID']
    content_ids = CONFIG['CONTENT_IDS']
    cache_file = CONFIG['CACHE_FILE']

    while True:
        print(f"Fetching data with offset {offset}...")
        items = fetch_data(user_id,cookies, offset, sort_direction)
        video_count = 0
        batch_start_time = time.time()
        for item in items:
            if item['contentId'] in content_ids:
                print(f"Skipping previously downloaded item: {item.get('contentTitle', 'Untitled')}")
                continue
            if max_clips > 0 and total_downloaded >= max_clips:
                print(f"Reached the specified number of clips ({max_clips}). Stopping download.")
                exit(0)

            if 'contentUrl' in item and 'publishedAt' in item:
                try:
                    content_title = item.get('contentTitle', 'Untitled')
                    content_url = item['contentUrl']
                    published_at = item['publishedAt']
                    
                    # Convert the publishedAt timestamp to a date string
                    date_str = convert_timestamp_to_date(published_at)
                    
                    # Format filename with title and date
                    sanitized_title = sanitize_filename(content_title)
                    title_format = CONFIG['TITLE_FORMAT']
                    filename = f"{title_format.format(date=date_str, title=sanitized_title)}.mp4"
                    
                    if filename in processed_files:
                        print(f"Skipping previously downloaded item: {item.get('contentTitle', 'Untitled')}")
                        continue    
                    download_mp4(download_folder, cookies, content_url, filename)
                    processed_files.add(filename)
                    update_cache(item["contentId"], cache_file)
                    video_count += 1
                    total_downloaded += 1
                    
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
            exit(0)
