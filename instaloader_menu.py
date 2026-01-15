#!/usr/bin/env python3
"""
Interactive Instaloader helper for downloading profiles, posts, videos, and stories.
Docs: https://instaloader.github.io/
"""

from __future__ import annotations

import os
import sys
from getpass import getpass
from typing import Any, Dict, Optional

try:
    import instaloader
except ImportError:  # pragma: no cover - runtime dependency
    print("Missing dependency: instaloader. Install with `pip install instaloader`.")
    sys.exit(1)


DEFAULT_CONFIG: Dict[str, Any] = {
    "download_comments": False,
    "download_geotags": False,
    "download_video_thumbnails": True,
    "save_metadata": True,
    "compress_json": True,
}
SESSION_DIR_NAME = ".instaloader_session"
SESSION_SUFFIX = ".session"

BANNER = r"""
 _   _ _   _ ____  _____ _____ _   _
| | | | \ | / ___|| ____| ____| \ | |
| | | |  \| \___ \|  _| |  _| |  \| |
| |_| | |\  |___) | |___| |___| |\  |
 \___/|_| \_|____/|_____|_____|_| \_|
"""

ACCENT = "\033[96m"
RESET = "\033[0m"


def prompt(text: str, default: Optional[str] = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{text}{suffix}: ").strip()
    return value or (default or "")


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def build_loader(base_dir: str, config: Dict[str, Any]) -> instaloader.Instaloader:
    loader = instaloader.Instaloader(
        download_comments=config["download_comments"],
        download_geotags=config["download_geotags"],
        download_video_thumbnails=config["download_video_thumbnails"],
        save_metadata=config["save_metadata"],
        compress_json=config["compress_json"],
        download_pictures=True,
        download_videos=True,
        quiet=False,
    )
    loader.dirname_pattern = os.path.join(base_dir, "{target}")
    return loader


def clear_screen() -> None:
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    clear_screen()
    print(f"{ACCENT}{BANNER}{RESET}")
    print("Instaloader Menu\n")


class TemporaryDirnamePattern:
    def __init__(self, loader: instaloader.Instaloader, pattern: str) -> None:
        self.loader = loader
        self.pattern = pattern
        self.original = loader.dirname_pattern

    def __enter__(self) -> None:
        self.original = self.loader.dirname_pattern
        self.loader.dirname_pattern = self.pattern

    def __exit__(self, exc_type, exc, tb) -> None:
        self.loader.dirname_pattern = self.original


def repo_root() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def session_dir(root_dir: str) -> str:
    return ensure_dir(os.path.join(root_dir, SESSION_DIR_NAME))


def session_file_for(session_root: str, username: str) -> str:
    return os.path.join(session_root, f"{username}{SESSION_SUFFIX}")


def last_user_path(session_root: str) -> str:
    return os.path.join(session_root, "last_user.txt")


def read_last_user(session_root: str) -> Optional[str]:
    path = last_user_path(session_root)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as handle:
        username = handle.read().strip()
    return username or None


def write_last_user(session_root: str, username: str) -> None:
    path = last_user_path(session_root)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(username)


def load_session_if_available(
    loader: instaloader.Instaloader, session_root: str
) -> Optional[str]:
    username = read_last_user(session_root)
    if username:
        file_path = session_file_for(session_root, username)
        if os.path.isfile(file_path):
            try:
                loader.load_session_from_file(username, filename=file_path)
                print(f"Loaded saved session for {username}.")
                return username
            except Exception:
                print("Saved session could not be loaded. Please log in again.")
                return None

    session_files = [
        name
        for name in os.listdir(session_root)
        if name.endswith(SESSION_SUFFIX)
    ]
    if len(session_files) == 1:
        username = session_files[0][: -len(SESSION_SUFFIX)]
        file_path = os.path.join(session_root, session_files[0])
        try:
            loader.load_session_from_file(username, filename=file_path)
            print(f"Loaded saved session for {username}.")
            return username
        except Exception:
            print("Saved session could not be loaded. Please log in again.")
            return None
    return None


def login_and_save_session(
    loader: instaloader.Instaloader, session_root: str
) -> Optional[str]:
    username = prompt("Instagram username for login (leave blank to skip)", default="")
    if not username:
        return None
    password = getpass("Password: ")
    try:
        loader.login(username, password)
        print("Login successful.")
        file_path = session_file_for(session_root, username)
        loader.save_session_to_file(filename=file_path)
        write_last_user(session_root, username)
        return username
    except instaloader.TwoFactorAuthRequiredException:
        code = prompt("Two-factor code")
        loader.two_factor_login(code)
        print("Login successful (2FA).")
        file_path = session_file_for(session_root, username)
        loader.save_session_to_file(filename=file_path)
        write_last_user(session_root, username)
        return username
    except instaloader.exceptions.BadCredentialsException:
        print("Login failed: bad credentials.")
        return None


def get_profile(loader: instaloader.Instaloader, username: str) -> Optional[instaloader.Profile]:
    try:
        return instaloader.Profile.from_username(loader.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile not found: {username}")
        return None
    except instaloader.exceptions.PrivateProfileNotFollowedException:
        print("Profile is private. Login and follow the account, then try again.")
        return None


def download_profile_all(loader: instaloader.Instaloader) -> None:
    username = prompt("Target profile username")
    profile = get_profile(loader, username)
    if not profile:
        return
    target = os.path.join(profile.username, "posts")
    downloaded = 0
    for post in profile.get_posts():
        loader.download_post(post, target=target)
        downloaded += 1
    print(f"Done. Downloaded {downloaded} posts.")


def download_profile_videos(loader: instaloader.Instaloader) -> None:
    username = prompt("Target profile username")
    profile = get_profile(loader, username)
    if not profile:
        return
    downloaded = 0
    target = os.path.join(profile.username, "videos")
    for post in profile.get_posts():
        if getattr(post, "is_video", False):
            loader.download_post(post, target=target)
            downloaded += 1
    print(f"Done. Downloaded {downloaded} video posts.")


def download_profile_stories(loader: instaloader.Instaloader, base_dir: str) -> None:
    if not loader.context.is_logged_in:
        print("Stories require login.")
        return
    username = prompt("Target profile username")
    profile = get_profile(loader, username)
    if not profile:
        return
    pattern = os.path.join(base_dir, "{target}", "stories")
    with TemporaryDirnamePattern(loader, pattern):
        loader.download_stories(userids=[profile.userid])
    print("Done.")


def download_profile_highlights(loader: instaloader.Instaloader, base_dir: str) -> None:
    if not loader.context.is_logged_in:
        print("Highlights require login.")
        return
    username = prompt("Target profile username")
    profile = get_profile(loader, username)
    if not profile:
        return
    pattern = os.path.join(base_dir, "{target}", "highlights")
    with TemporaryDirnamePattern(loader, pattern):
        loader.download_highlights(profile)
    print("Done.")


def download_hashtag(loader: instaloader.Instaloader) -> None:
    tag = prompt("Hashtag (without #)")
    try:
        hashtag = instaloader.Hashtag.from_name(loader.context, tag)
    except instaloader.exceptions.QueryReturnedNotFoundException:
        print(f"Hashtag not found: {tag}")
        return
    target = os.path.join("hashtags", tag)
    for post in hashtag.get_posts():
        loader.download_post(post, target=target)
    print("Done.")


def download_shortcode(loader: instaloader.Instaloader) -> None:
    shortcode = prompt("Post shortcode (e.g., CxY...)")
    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
    except instaloader.exceptions.QueryReturnedNotFoundException:
        print(f"Post not found: {shortcode}")
        return
    target = os.path.join("shortcodes", shortcode)
    loader.download_post(post, target=target)
    print("Done.")


def toggle_setting(config: Dict[str, Any]) -> None:
    keys = list(config.keys())
    while True:
        print("\nSettings:")
        for idx, key in enumerate(keys, start=1):
            print(f"  {idx}. {key} = {config[key]}")
        print("  0. Back")
        choice = prompt("Select setting to toggle", default="0")
        if choice == "0":
            return
        try:
            index = int(choice) - 1
            if index < 0 or index >= len(keys):
                raise ValueError
        except ValueError:
            print("Invalid choice.")
            continue
        key = keys[index]
        if isinstance(config[key], bool):
            config[key] = not config[key]
        else:
            print("Only boolean settings can be toggled here.")


def main() -> None:
    print_banner()
    base_dir = ensure_dir(prompt("Download directory", default="downloads"))
    config = dict(DEFAULT_CONFIG)
    loader = build_loader(base_dir, config)
    session_root = session_dir(repo_root())

    active_user = load_session_if_available(loader, session_root)
    if not loader.context.is_logged_in:
        active_user = login_and_save_session(loader, session_root)

    while True:
        print_banner()
        print(f"Download directory: {base_dir}")
        if loader.context.is_logged_in:
            print(f"Logged in as: {loader.context.username}\n")
        else:
            print("Not logged in\n")
        print(
            "Main Menu\n"
            "  1. Download profile (all posts, reels, videos)\n"
            "  2. Download profile videos (includes reels)\n"
            "  3. Download profile stories\n"
            "  4. Download profile highlights\n"
            "  5. Download hashtag\n"
            "  6. Download post by shortcode\n"
            "  7. Settings\n"
            "  0. Exit"
        )
        choice = prompt("Select option", default="0")
        if choice == "1":
            download_profile_all(loader)
        elif choice == "2":
            download_profile_videos(loader)
        elif choice == "3":
            download_profile_stories(loader, base_dir)
        elif choice == "4":
            download_profile_highlights(loader, base_dir)
        elif choice == "5":
            download_hashtag(loader)
        elif choice == "6":
            download_shortcode(loader)
        elif choice == "7":
            toggle_setting(config)
            loader = build_loader(base_dir, config)
            if active_user:
                file_path = session_file_for(session_root, active_user)
                if os.path.isfile(file_path):
                    try:
                        loader.load_session_from_file(active_user, filename=file_path)
                    except Exception:
                        print("Saved session could not be loaded after settings change.")
        elif choice == "0":
            print("Goodbye.")
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
