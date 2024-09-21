import os
from helpers import parse_cookies,load_cache,load_config
from requestHelper import fetch_user_id

def parse_config():
    # Load configuration
    config = load_config()
    # Get user ID from username
    username = config['username']
    cookies = parse_cookies(config.get('cookies', []))
    user_id = fetch_user_id(username, cookies)
    cache_file = config.get('cacheFile', '')
    download_folder = config.get('downloadFolder', 'downloads')
    title_format = config.get('titleFormat', '{date}_{title}')
    max_clips = config.get('maxClips', 0)
    sort_direction = config.get('sortDirection', '')

    if not user_id:
        print(f"Could not fetch user ID for username: {username}. Please refer to the README for setup instructions: https://github.com/Dave-Swagten/Medal.tv-Bulk-Downloader?tab=readme-ov-file#%EF%B8%8F-configuration")
        exit(1)

    print(f"Fetched User ID: {user_id} for username: {username}")


    # User input for sorting order
    while sort_direction == '':
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
    while max_clips < 0:
        try:
            max_clips = int(input("Enter the number of clips to download (0 for all): "))
            if max_clips < 0:
                print("Please enter a non-negative number.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    return {
        "COOKIES": cookies,
        "CONTENT_IDS": load_cache(cache_file),
        "USER_ID": user_id,
        "USERNAME": username,
        "CACHE_FILE": cache_file,
        "MAX_CLIPS": max_clips,
        "SORT_DIRECTION": sort_direction,
        "DOWNLOAD_FOLDER": download_folder,
        "TITLE_FORMAT": title_format
    }

