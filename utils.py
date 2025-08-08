from instagrapi import Client
import requests
import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

def generate_session() -> bool:
    """Generate Instagram session with user credentials."""
    try:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        otp_from_totp = input("Enter your OTP: ").strip()
        
        if not all([username, password, otp_from_totp]):
            print("All fields are required!")
            return False
        
        client = Client()
        client.delay_range = [1, 10]
        client.login(username, password, False, otp_from_totp)
        client.dump_settings("session.json")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def ensure_directory_exists(directory_path: str) -> None:
    """Create directory if it doesn't exist."""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def download_file(url: str, file_path: str, max_retries: int = 3) -> bool:
    """Download a file from URL with retry logic."""
    if os.path.exists(file_path):
        return True
        
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed to download {url}: {e}")
                return False
            print(f"Download attempt {attempt + 1} failed, retrying...")
    
    return False

def generate_user_info_file(target: str, user_info: Any) -> bool:
    """Generate user info JSON file and download profile picture."""
    try:
        # Create user info dictionary
        user_data = {}
        for attr_name in dir(user_info):
            if not attr_name.startswith('_') and not callable(getattr(user_info, attr_name)):
                value = getattr(user_info, attr_name)
                # Handle various data types
                if isinstance(value, (str, int, float, bool, type(None))):
                    user_data[attr_name] = value
                else:
                    user_data[attr_name] = str(value)
        
        # Save as JSON
        json_path = os.path.join(target, 'user_info.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False, default=str)
        
        # Download profile picture
        profile_pic_path = os.path.join(target, f'{target}.jpg')
        if hasattr(user_info, 'profile_pic_url_hd') and user_info.profile_pic_url_hd:
            return download_file(user_info.profile_pic_url_hd, profile_pic_path)
        
        return True
    except Exception as e:
        print(f"Error generating user info file: {e}")
        return False

def user_summary(user_info: Any) -> None:
    """Display formatted user summary information."""
    try:
        username = getattr(user_info, 'username', 'N/A')
        full_name = getattr(user_info, 'full_name', 'N/A')
        follower_count = getattr(user_info, 'follower_count', 0)
        following_count = getattr(user_info, 'following_count', 0)
        media_count = getattr(user_info, 'media_count', 0)
        biography = getattr(user_info, 'biography', 'No bio available')
        
        print(f"Summary for '{username}'")
        print("=" * 50)
        print(f"Full Name: {full_name}")
        print(f"Followers: {follower_count:,}")
        print(f"Following: {following_count:,}")
        print(f"Posts: {media_count:,}")
        print(f"\nBiography:")
        print("-" * 20)
        print(biography or "No biography available")
        print("-" * 20)
        print(f"\nDetailed information saved to: {username}/user_info.json")
        print("=" * 50)
    except Exception as e:
        print(f"Error displaying user summary: {e}")


def media_sorter(media: List[Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Sort media items by type and extract relevant information."""
    media_categories = {
        "images": [],    # media_type=1
        "videos": [],    # media_type=2 and product_type=feed
        "igtv": [],      # media_type=2 and product_type=igtv
        "reels": [],     # media_type=2 and product_type=clips
        "albums": []     # media_type=8
    }
    
    for item in media:
        try:
            # Common fields for all media types
            base_data = {
                "id": getattr(item, 'id', ''),
                "code": getattr(item, 'code', ''),
                "taken_time": getattr(item, 'taken_at', '').strftime("%d-%m-%Y %H %M %S %Z") if hasattr(item, 'taken_at') else '',
                "likes": getattr(item, 'like_count', 0),
                "comment_count": getattr(item, 'comment_count', 0),
                "caption": getattr(item, 'caption_text', '') or ''
            }
            
            media_type = getattr(item, 'media_type', 0)
            product_type = getattr(item, 'product_type', '')
            
            if media_type == 1:  # Images
                media_categories["images"].append({
                    **base_data,
                    "url": getattr(item, 'thumbnail_url', '')
                })
                
            elif media_type == 2:  # Videos
                video_data = {
                    **base_data,
                    "url": getattr(item, 'video_url', ''),
                    "view_count": getattr(item, 'view_count', 0)
                }
                
                if product_type == "feed":
                    media_categories["videos"].append(video_data)
                elif product_type == "igtv":
                    media_categories["igtv"].append(video_data)
                elif product_type == "clips":
                    media_categories["reels"].append({
                        **video_data,
                        "thumbnail_url": getattr(item, 'thumbnail_url', ''),
                        "view_count": getattr(item, 'play_count', 0)  # Reels use play_count
                    })
                    
            elif media_type == 8:  # Albums
                album_urls = []
                resources = getattr(item, 'resources', [])
                
                for resource in resources:
                    resource_type = getattr(resource, 'media_type', 0)
                    if resource_type == 1:  # Image in album
                        url = getattr(resource, 'thumbnail_url', '')
                    elif resource_type == 2:  # Video in album
                        url = getattr(resource, 'video_url', '')
                    else:
                        continue
                    
                    if url:
                        album_urls.append(url)
                
                media_categories["albums"].append({
                    **base_data,
                    "urls": album_urls
                })
                
        except Exception as e:
            print(f"Error processing media item: {e}")
            continue
    
    return media_categories

def save_media_metadata(media_item: Dict[str, Any], file_path: str) -> None:
    """Save media metadata to a text file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for key, value in media_item.items():
                if key != 'urls':  # Skip URLs list for albums
                    f.write(f'{key}: {value}\n')
    except Exception as e:
        print(f"Error saving metadata to {file_path}: {e}")

def media_downloader(media_data: Dict[str, List[Dict[str, Any]]], target: str) -> None:
    """Download media files organized by type."""
    base_path = os.path.join(target, 'posts')
    
    for media_type, items in media_data.items():
        if not items:  # Skip empty categories
            continue
            
        print(f"Downloading {len(items)} {media_type}...")
        type_path = os.path.join(base_path, media_type)
        
        for item in items:
            try:
                item_name = f'{item["taken_time"]} - {item["id"]}'
                
                if media_type == "images":
                    media_file = os.path.join(type_path, f'{item_name}.jpg')
                    metadata_file = os.path.join(type_path, f'{item_name}.txt')
                    
                    if download_file(item["url"], media_file):
                        save_media_metadata(item, metadata_file)
                        
                elif media_type in ["videos", "igtv", "reels"]:
                    media_file = os.path.join(type_path, f'{item_name}.mp4')
                    metadata_file = os.path.join(type_path, f'{item_name}.txt')
                    
                    if download_file(item["url"], media_file):
                        save_media_metadata(item, metadata_file)
                        
                elif media_type == "albums":
                    album_dir = os.path.join(type_path, item_name)
                    ensure_directory_exists(album_dir)
                    
                    metadata_file = os.path.join(album_dir, f'{item_name}.txt')
                    save_media_metadata(item, metadata_file)
                    
                    # Download album media
                    for idx, url in enumerate(item.get("urls", []), 1):
                        # Determine file extension based on URL or content type
                        extension = '.mp4' if 'video' in url or url.endswith('.mp4') else '.jpg'
                        album_media_file = os.path.join(album_dir, f'{idx}{extension}')
                        download_file(url, album_media_file)
                        
            except Exception as e:
                print(f"Error downloading {media_type} item: {e}")
                continue


def media_downloader_tagged(media_data: Dict[str, List[Dict[str, Any]]], target: str) -> None:
    """Download tagged media files organized by type."""
    base_path = os.path.join(target, 'tagged_posts')
    
    for media_type, items in media_data.items():
        if not items:  # Skip empty categories
            continue
            
        print(f"Downloading {len(items)} tagged {media_type}...")
        type_path = os.path.join(base_path, media_type)
        
        for item in items:
            try:
                item_name = f'{item["taken_time"]} - {item["id"]}'
                
                if media_type == "images":
                    media_file = os.path.join(type_path, f'{item_name}.jpg')
                    metadata_file = os.path.join(type_path, f'{item_name}.txt')
                    
                    if download_file(item["url"], media_file):
                        save_media_metadata(item, metadata_file)
                        
                elif media_type in ["videos", "igtv", "reels"]:
                    media_file = os.path.join(type_path, f'{item_name}.mp4')
                    metadata_file = os.path.join(type_path, f'{item_name}.txt')
                    
                    if download_file(item["url"], media_file):
                        save_media_metadata(item, metadata_file)
                        
                elif media_type == "albums":
                    album_dir = os.path.join(type_path, item_name)
                    ensure_directory_exists(album_dir)
                    
                    metadata_file = os.path.join(album_dir, f'{item_name}.txt')
                    save_media_metadata(item, metadata_file)
                    
                    # Download album media
                    for idx, url in enumerate(item.get("urls", []), 1):
                        # Determine file extension based on URL or content type
                        extension = '.mp4' if 'video' in url or url.endswith('.mp4') else '.jpg'
                        album_media_file = os.path.join(album_dir, f'{idx}{extension}')
                        download_file(url, album_media_file)
                        
            except Exception as e:
                print(f"Error downloading tagged {media_type} item: {e}")
                continue
