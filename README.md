# Unseen

```
 _   _ _   _ ____  _____ _____ _   _
| | | | \ | / ___|| ____| ____| \ | |
| | | |  \| \___ \|  _| |  _| |  \| |
| |_| | |\  |___) | |___| |___| |\  |
 \___/|_| \_|____/|_____|_____|_| \_|
```

Interactive CLI for downloading Instagram content with Instaloader.

## Features

- Profile downloads: posts, videos (incl. reels), stories, highlights, and profile picture.
- Hashtag downloads and single post download by shortcode.
- Followers/following list export.
- Saved posts download (login required, your own account).
- Toggle metadata, comments, geotags, pictures, videos, and video thumbnails.
- Max items per download and fast-update behavior.

## Folder Layout

Default base directory is `downloads/`. Targets are organized as:

- `downloads/<username>/posts/`
- `downloads/<username>/videos/`
- `downloads/<username>/stories/`
- `downloads/<username>/highlights/<highlight_title>/`
- `downloads/<username>/saved/`
- `downloads/hashtags/<tag>/`
- `downloads/shortcodes/<shortcode>/`

Sessions are saved under:

- `.instaloader_session/` in the repo root
- `.instaloader_session/errors.log` stores error traces for failed actions

## Requirements

- Python 3.8+
- `instaloader` (see `requirements.txt`)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

```bash
python unseen.py
```

You can log in from the menu to access private content you follow, stories, and highlights.

## Walkthrough

1. Run `python unseen.py`.
2. Choose a download directory (default `downloads`).
3. Log in if you need private content or saved posts.
4. Set a target profile when prompted.
5. Use the main menu to download content or adjust settings.

## Notes

- Downloads are saved under the directory you choose at startup.
- Some actions require login (stories, highlights, private profiles).
- Use responsibly and follow Instagram's terms and Instaloader documentation.

## Troubleshooting

- Login/2FA issues: try logging in again from Settings, verify 2FA code, and ensure Instaloader is up to date.
- Private profile errors: you must be logged in and follow the profile.
- Rate limits (429/too many requests): pause and retry later; reduce download volume.
- Session problems: delete `.instaloader_session/` and re-login.

## Disclaimer

This project is provided as-is. You are responsible for how you use it and for complying with all applicable laws,
platform policies, and terms of service. The authors are not liable for any account restrictions, flags, or bans that
may result from use of this tool. Use it ethically, respect privacy, and avoid excessive or abusive downloading.

## Future Work

### Must haves

- Robust error classification with user-friendly guidance (rate limits, login required, private account).
- Retry/backoff and pause controls for rate limits and temporary failures.
- Saved configuration profile (persist settings between runs).

### Nice to haves

- Optional limits per download type (posts vs. reels vs. stories).
- Export followers/following with extra fields (full name, user id) and CSV support.
- Progress summary per action (downloaded/skipped/failed counts).
- Session selection when multiple accounts exist.

### Completely optional changes, but boy would it be awesome to have them

- Rich TUI (panels, tables, live progress) with `rich`.
- Scheduling mode (run nightly/weekly tasks).
- Plug-in system for custom download targets or pipelines.
