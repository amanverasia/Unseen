# Unseen (Instaloader CLI)

## Overview

Unseen is a Python CLI wrapper around Instaloader that provides a menu-driven interface for downloading Instagram
content.

## Entry Point

- `unseen.py`

## Features

- Profile downloads: posts, videos (incl. reels), stories, highlights
- Hashtag downloads
- Single post download by shortcode
- Session persistence (saved in repo root)
- Config toggles for metadata, comments, geotags, video thumbnails

## Folder Layout

Default base directory is `downloads/`. Targets are organized as:

- `downloads/<username>/posts/`
- `downloads/<username>/videos/`
- `downloads/<username>/stories/`
- `downloads/<username>/highlights/<highlight_title>/`
- `downloads/hashtags/<tag>/`
- `downloads/shortcodes/<shortcode>/`

Sessions are saved under:

- `.instaloader_session/` in the repo root

## Setup and Run

```bash
pip install -r requirements.txt
python unseen.py
```

## Notes

- Stories and highlights require login.
- Session files are ignored by git for safety.
