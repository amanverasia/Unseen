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
- Interactive CLI menu system with 8 options
- Session management with `session.json` file
- Automatic directory structure creation for target data
- Handles Instagram login with 2FA/TOTP authentication

### Utility Functions (`utils.py`)
Key functions:
- `generate_session()` - Creates Instagram session with 2FA login
- `media_sorter()` - Categorizes media by type (images, videos, igtv, reels, albums)
- `media_downloader()` - Downloads regular posts to `/posts/` subdirectories
- `media_downloader_tagged()` - Downloads tagged media to `/tagged_posts/`
- `generate_user_info_file()` - Extracts user profile data and profile picture
- `user_summary()` - Displays formatted user statistics

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
- Requires TOTP-based 2FA (not SMS) for authentication
- Session persistence through `session.json` file
- Handles rate limiting and Instagram's anti-bot measures

## Important Security Notes

- Never commit `session.json` files to version control
- This tool requires Instagram credentials and operates in a legal grey area
- Users must comply with Instagram's Terms of Service
- Tool includes disclaimer about potential account bans