import time
from config import CONFIG
from helpers import format_filename, update_cache
from requestHelper import download_mp4, fetch_data

if __name__ == "__main__":
    offset = 0
    total_downloaded = 0
    max_clips = CONFIG['MAX_CLIPS']
    content_ids = CONFIG['CONTENT_IDS']

    while True:
        print(f"Fetching data with offset {offset}...")
        items = fetch_data(offset)
        video_count = len(items)
        if video_count == 0:
            print("No more videos to download. Exiting.")
            break
        batch_start_time = time.time()
        for item in items:
            if item['contentId'] in content_ids:
                print(f"Skipping previously downloaded item: {item.get('contentTitle', 'Untitled')}")
                continue
            if max_clips > 0 and total_downloaded >= max_clips:
                print(f"Reached the specified number of clips ({max_clips}). Stopping download.")
                exit(0)

            if 'contentUrl' in item and 'publishedAt' in item and 'contentId' in item:
                try:
                    filename = format_filename(item.get('contentTitle', 'Untitled'), item['publishedAt'])
                    content_url = item['contentUrl']
                    content_id = item["contentId"]

                    download_mp4(content_url, filename)
                    content_ids.add(content_id)
                    update_cache(content_id)
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
            break
