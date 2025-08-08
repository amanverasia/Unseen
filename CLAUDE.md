# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UNSEEN is a Python-based Instagram data extraction tool that allows users to download media, analyze follower relationships, and extract profile information. The tool uses the instagrapi library for Instagram API interactions and requires 2FA authentication.

## Setup and Dependencies

Install dependencies:
```bash
# Unix-based systems
pip3 install -r requirements.txt

# Windows
pip install -r requirements.txt
```

Required packages:
- `instagrapi` - Instagram private API client
- `requests` - HTTP library for downloading media files

## Running the Application

```bash
# Unix-based systems
python3 main.py

# Windows  
python main.py
```

## Core Architecture

### Main Application (`main.py`)
- Interactive CLI menu system with 11 options including granular media download options
- Class-based `InstagramTool` architecture for better organization
- Session management with `session.json` file
- Automatic directory structure creation for target data
- Handles Instagram login with 2FA/TOTP authentication
- Supports separate downloads for posts, reels, and videos

### Utility Functions (`utils.py`)
Key functions:
- `generate_session()` - Creates Instagram session with 2FA login
- `media_sorter()` - Categorizes media by type (images, videos, igtv, reels, albums) with updated reels handling
- `media_downloader()` - Downloads regular posts to `/posts/` subdirectories with retry logic
- `media_downloader_tagged()` - Downloads tagged media to `/tagged_posts/` 
- `generate_user_info_file()` - Extracts user profile data and profile picture using proper JSON formatting
- `user_summary()` - Displays formatted user statistics
- `download_file()` - Utility function with retry logic for reliable file downloads
- `ensure_directory_exists()` - Creates directory structures as needed

### Legacy Scripts Directory
Contains standalone Python scripts using `instaloader` library for:
- Finding common followers between users
- Finding common following relationships  
- Generating relationship graphs
- Individual user follower/following extraction

## Data Organization

Target data is organized in directories named after the Instagram username:
```
{target_username}/
├── posts/
│   ├── images/
│   ├── videos/
│   ├── igtv/
│   ├── reels/
│   └── albums/
├── tagged_posts/
│   └── [same structure as posts]
├── highlights/
│   └── {count} {highlight_id}/
├── followers.txt
├── following.txt
├── user_info.json
└── {username}.jpg (profile picture)
```

## Instagram API Integration

- Uses `instagrapi.Client` for API interactions with configurable delay ranges (3-10 seconds)
- **Reels Handling**: Uses `user_clips_v1()` method for fetching reels with `product_type: 'clips'`
- **Media Separation**: 
  - Posts (images/albums): `user_medias_v1()` filtered for `media_type: 1` and `media_type: 8`
  - Regular Videos: `user_medias_v1()` filtered for `media_type: 2` with `product_type: 'feed'` or `'igtv'`
  - Reels: `user_clips_v1()` for `media_type: 2` with `product_type: 'clips'`
- Requires TOTP-based 2FA (not SMS) for authentication
- Session persistence through `session.json` file
- Handles rate limiting and Instagram's anti-bot measures
- Enhanced error handling and retry logic for downloads

## Important Security Notes

- Never commit `session.json` files to version control
- This tool requires Instagram credentials and operates in a legal grey area
- Users must comply with Instagram's Terms of Service
- Tool includes disclaimer about potential account bans