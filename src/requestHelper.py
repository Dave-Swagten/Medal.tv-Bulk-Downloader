import os
import time
import requests

# Fetch user ID from username
def fetch_user_id(username, cookies):
    url = f"https://medal.tv/api/users?username={username}"
    try:
        response = requests.get(url, cookies=cookies)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                return data[0].get('userId')
        print(f"Failed to fetch user ID for username: {username}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching user ID: {e}")
    return None

def fetch_data(user_id, cookies, offset, sort_direction):
    try:
        url = f"https://medal.tv/api/content?userId={user_id}&limit=100&offset={offset}&sortBy=publishedAt&sortDirection={sort_direction}"
        response = requests.get(url, cookies=cookies)
        if response.status_code == 200:
             data = response.json()
        else:
            print(f"Failed to fetch data from API with offset {offset}. Status code: {response.status_code}")
            data = None
    except Exception as e:
        print(f"Error fetching data from API with offset {offset}: {e}")
        data = None
    
    if not data:
        print("No data returned or error occurred. Exiting.")
        exit(1)
        
    if not isinstance(data, list):
        print(f"Unexpected data format. Expected list but got {type(data)}.")
        exit(1)
    return data

def download_mp4(download_folder, cookies, content_url, filename):
    try:
        filepath = os.path.join(download_folder, filename)
        
        # Check if the file already exists in the download folder
        if os.path.exists(filepath):
            print(f"File already exists: {filepath}")
            return
        
        print(f"Starting down of {filename}")
        # Sleep for 1 second before making the request (to prevent rate limit errors)
        time.sleep(1)
        
        response = requests.get(content_url, cookies=cookies)
        
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded clip to {filepath}")
        else:
            print(f"Failed to download {content_url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {content_url}: {e}")
