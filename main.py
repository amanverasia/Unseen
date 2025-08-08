from utils import (
    generate_session, media_sorter, generate_user_info_file, 
    user_summary, media_downloader, media_downloader_tagged,
    download_file, ensure_directory_exists
)
from instagrapi import Client
import os
import pickle
import json
from typing import Dict, List, Any, Optional

class InstagramTool:
    def __init__(self):
        self.client: Optional[Client] = None
        self.target: str = ""
        self.user_id: Optional[str] = None
        self.session_exists: bool = False
        
    def initialize_client(self) -> bool:
        """Initialize Instagram client and load session if available."""
        try:
            self.client = Client()
            self.client.delay_range = [3, 10]
            if os.path.exists("session.json"):
                self.client.load_settings("session.json")
                self.session_exists = True
                return True
            return False
        except Exception as e:
            print(f"Error initializing client: {e}")
            return False
            
    def generate_user_id(self) -> bool:
        """Generate user ID from username."""
        if not self.client:
            return False
        try:
            print('Generating user id... This might take a few seconds.')
            self.user_id = self.client.user_id_from_username(self.target)
            print('User ID Generated successfully!')
            return True
        except Exception as e:
            print(f"Error generating user ID: {e}")
            return False

    def save_followers(self) -> bool:
        """Save followers list to file."""
        if not self.client or not self.user_id:
            return False
        try:
            followers_data = self.client.user_followers(self.user_id)
            file_path = os.path.join(self.target, 'followers.txt')
            with open(file_path, 'w', encoding="utf-8") as fh:
                for follower in followers_data.values():
                    fh.write(f'Username: "{follower.username}" ')
                    fh.write(f'Full Name: "{follower.full_name}" ')
                    fh.write(f'Profile Picture: "{follower.profile_pic_url}"\n')
            return True
        except Exception as e:
            print(f"Error saving followers: {e}")
            return False

    def save_following(self) -> bool:
        """Save following list to file."""
        if not self.client or not self.user_id:
            return False
        try:
            following_data = self.client.user_following(self.user_id)
            file_path = os.path.join(self.target, 'following.txt')
            with open(file_path, 'w', encoding="utf-8") as fh:
                for following in following_data.values():
                    fh.write(f'Username: "{following.username}" ')
                    fh.write(f'Full Name: "{following.full_name}" ')
                    fh.write(f'Profile Picture: "{following.profile_pic_url}"\n')
            return True
        except Exception as e:
            print(f"Error saving following: {e}")
            return False

    def fetch_user_media(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch and combine all user media (posts and clips)."""
        if not self.client or not self.user_id:
            return {}
        try:
            posts_media = self.client.user_medias_v1(self.user_id)
            clips_media = self.client.user_clips_v1(self.user_id)
            
            sorted_posts = media_sorter(posts_media)
            sorted_clips = media_sorter(clips_media)
            
            return self._combine_media(sorted_posts, sorted_clips)
        except Exception as e:
            print(f"Error fetching user media: {e}")
            return {}

    def fetch_tagged_media(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch tagged media for user."""
        if not self.client or not self.user_id:
            return {}
        try:
            tagged_media = self.client.usertag_medias_v1(self.user_id)
            return media_sorter(tagged_media)
        except Exception as e:
            print(f"Error fetching tagged media: {e}")
            return {}

    def download_highlights(self) -> bool:
        """Download user highlights."""
        if not self.client or not self.user_id:
            return False
        try:
            highlights = self.client.user_highlights(self.user_id)
            highlights_dir = os.path.join(self.target, "highlights")
            
            for count, highlight in enumerate(highlights):
                highlight_dir = os.path.join(highlights_dir, f"{count+1} {highlight.pk}")
                ensure_directory_exists(highlight_dir)
                
                # Download cover image
                cover_path = os.path.join(highlight_dir, 'cover.jpg')
                cover_url = highlight.cover_media['cropped_image_version']['url']
                download_file(cover_url, cover_path)
                
                # Save highlight info
                info_path = os.path.join(highlight_dir, f'{count+1} {highlight.pk}.txt')
                with open(info_path, "w", encoding="utf-8") as fh:
                    fh.write(f"Title: {highlight.title}\n")
                    fh.write(f"Highlight ID: {highlight.pk}\n")
                    fh.write(f"Created at: {highlight.created_at}\n")
                    fh.write(f"Media Count: {highlight.media_count}\n")
                    fh.write(f"Cover Image: {cover_url}\n")
                
                # Download highlight media
                highlight_info = self.client.highlight_info(highlight.pk)
                media_list = []
                
                for media_count, media in enumerate(highlight_info.items):
                    media_num = media_count + 1
                    if media.media_type == 1:  # Image
                        file_path = os.path.join(highlight_dir, f'{media_num}.jpg')
                        download_file(media.thumbnail_url, file_path)
                        media_list.append([media_num, media.thumbnail_url])
                    elif media.media_type == 2:  # Video
                        file_path = os.path.join(highlight_dir, f'{media_num}.mp4')
                        download_file(media.video_url, file_path)
                        media_list.append([media_num, media.video_url])
                
                # Save media list
                media_list_path = os.path.join(highlight_dir, 'highlight_media_list.txt')
                with open(media_list_path, "w", encoding="utf-8") as fh:
                    for item in media_list:
                        fh.write(f"{item}\n")
            
            # Save highlights data
            pickle_path = os.path.join(highlights_dir, "media.pickle")
            with open(pickle_path, "wb") as fh:
                pickle.dump(highlights, fh)
            
            return True
        except Exception as e:
            print(f"Error downloading highlights: {e}")
            return False

    def _combine_media(self, sorted_posts: Dict, sorted_clips: Dict) -> Dict:
        """Combine posts and clips media, avoiding duplicates."""
        combined = sorted_posts.copy()
        
        for key in combined:
            existing_ids = {item['id'] for item in combined[key]}
            for clip in sorted_clips.get(key, []):
                if clip['id'] not in existing_ids:
                    combined[key].append(clip)
        
        return combined

    def setup_directories(self) -> None:
        """Create necessary directory structure for target."""
        base_dirs = ['posts', 'tagged_posts', 'highlights']
        media_types = ['images', 'videos', 'igtv', 'reels', 'albums']
        
        ensure_directory_exists(self.target)
        
        for base_dir in base_dirs:
            dir_path = os.path.join(self.target, base_dir)
            ensure_directory_exists(dir_path)
            
            if base_dir in ['posts', 'tagged_posts']:
                for media_type in media_types:
                    media_dir = os.path.join(dir_path, media_type)
                    ensure_directory_exists(media_dir)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Display the application banner."""
    banner = '''                                                            
@@@  @@@  @@@  @@@   @@@@@@   @@@@@@@@  @@@@@@@@  @@@  @@@  
@@@  @@@  @@@@ @@@  @@@@@@@   @@@@@@@@  @@@@@@@@  @@@@ @@@  
@@!  @@@  @@!@!@@@  !@@       @@!       @@!       @@!@!@@@  
!@!  @!@  !@!!@!@!  !@!       !@!       !@!       !@!!@!@!  
@!@  !@!  @!@ !!@!  !!@@!!    @!!!:!    @!!!:!    @!@ !!@!  
!@!  !!!  !@!  !!!   !!@!!!   !!!!!:    !!!!!:    !@!  !!!  
!!:  !!!  !!:  !!!       !:!  !!:       !!:       !!:  !!!  
:!:  !:!  :!:  !:!      !:!   :!:       :!:       :!:  !:!  
::::: ::   ::   ::  :::: ::    :: ::::   :: ::::   ::   ::  
 : :  :   ::    :   :: : :    : :: ::   : :: ::   ::    :   
                                                            '''
    print(banner)
    print('\n')

def display_menu(target: str):
    """Display the main menu options."""
    clear_screen()
    display_banner()
    print(f'Current Target: "{target}"\n')
    print('Choose one of the following options:')
    print('1. Generate Session File and User ID')
    print('2. Summary of target')
    print('3. Find Followers')
    print('4. Find Following')
    print('5. Download All Media')
    print('6. Download All Tagged Media')
    print('7. Download All Highlights')
    print('8. Exit')

def get_valid_choice() -> str:
    """Get and validate user choice."""
    while True:
        choice = input('\nEnter Choice: ').strip()
        
        if not choice.isdigit():
            print('Invalid choice. Please enter a number between 1-8.')
            continue
            
        choice_num = int(choice)
        if not (1 <= choice_num <= 8):
            print('Invalid choice. Please enter a number between 1-8.')
            continue
            
        return choice

def save_media_data(media_data: Dict, target: str, media_type: str):
    """Save media data to pickle and text files."""
    base_path = os.path.join(target, media_type)
    
    # Save as pickle
    pickle_path = os.path.join(base_path, "media.pickle")
    with open(pickle_path, "wb") as fh:
        pickle.dump(media_data, fh)
    
    # Save as text
    text_path = os.path.join(base_path, "media.txt")
    with open(text_path, "w", encoding="utf-8") as fh:
        fh.write(str(media_data))

def wait_for_user():
    """Wait for user to press Enter."""
    input('\nPress Enter to continue...')

def main():
    """Main application entry point."""
    # Initialize the Instagram tool
    tool = InstagramTool()
    
    # Display banner and get target
    clear_screen()
    display_banner()
    tool.target = input('Please enter your target: ').strip()
    
    if not tool.target:
        print("Target username cannot be empty!")
        return
    
    # Initialize client
    tool.initialize_client()
    
    while True:
        display_menu(tool.target)
        choice = get_valid_choice()
        clear_screen()
        
        # Setup directories for all operations except exit
        if choice != '8':
            tool.setup_directories()
        
        if choice == '8':
            print("Goodbye!")
            break
            
        elif choice == '1':
            # Generate session and user ID
            if not os.path.exists("session.json"):
                if generate_session():
                    print('Session file successfully generated!')
                    tool.initialize_client()
                    wait_for_user()
                    if tool.generate_user_id():
                        wait_for_user()
                else:
                    print('Failed to generate session. Please try again.')
                    wait_for_user()
            else:
                print("Session file already exists.")
                print("If you want to create a new session, delete session.json and try again.")
                tool.initialize_client()
                wait_for_user()
                if tool.generate_user_id():
                    wait_for_user()
                    
        elif choice == '2':
            # User summary
            if not tool.session_exists:
                print('Please generate a session file first (Option 1).')
                wait_for_user()
                continue
                
            if not tool.user_id:
                if not tool.generate_user_id():
                    wait_for_user()
                    continue
                    
            try:
                user_info = tool.client.user_info(tool.user_id)
                generate_user_info_file(tool.target, user_info)
                user_summary(user_info)
                wait_for_user()
            except Exception as e:
                print(f"Error getting user info: {e}")
                wait_for_user()
                
        elif choice == '3':
            # Find followers
            if not tool.session_exists or not tool.user_id:
                print('Please generate session and user ID first (Option 1).')
                wait_for_user()
                continue
                
            print('Fetching followers... This might take a few minutes.')
            if tool.save_followers():
                print('Followers saved successfully!')
            else:
                print('Failed to save followers.')
            wait_for_user()
            
        elif choice == '4':
            # Find following
            if not tool.session_exists or not tool.user_id:
                print('Please generate session and user ID first (Option 1).')
                wait_for_user()
                continue
                
            print('Fetching following list... This might take a few minutes.')
            if tool.save_following():
                print('Following list saved successfully!')
            else:
                print('Failed to save following list.')
            wait_for_user()
            
        elif choice == '5':
            # Download all media
            if not tool.session_exists or not tool.user_id:
                print('Please generate session and user ID first (Option 1).')
                wait_for_user()
                continue
                
            print("Fetching all media... This might take a while.")
            media_data = tool.fetch_user_media()
            if media_data:
                save_media_data(media_data, tool.target, "posts")
                media_downloader(media_data, tool.target)
                print('Media download completed!')
            else:
                print('Failed to fetch media.')
            wait_for_user()
            
        elif choice == '6':
            # Download tagged media
            if not tool.session_exists or not tool.user_id:
                print('Please generate session and user ID first (Option 1).')
                wait_for_user()
                continue
                
            print("Fetching tagged media... This might take a while.")
            tagged_data = tool.fetch_tagged_media()
            if tagged_data:
                save_media_data(tagged_data, tool.target, "tagged_posts")
                media_downloader_tagged(tagged_data, tool.target)
                print('Tagged media download completed!')
            else:
                print('Failed to fetch tagged media.')
            wait_for_user()
            
        elif choice == '7':
            # Download highlights
            if not tool.session_exists or not tool.user_id:
                print('Please generate session and user ID first (Option 1).')
                wait_for_user()
                continue
                
            print("Downloading highlights... This might take a while.")
            if tool.download_highlights():
                print('Highlights download completed!')
            else:
                print('Failed to download highlights.')
            wait_for_user()

if __name__ == "__main__":
    main()

