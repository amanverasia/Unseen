from utils import generate_session, media_sorter, generate_user_info_file, user_summary, media_downloader
from instagrapi import Client
import os
import pickle

def user_followers(user_id):
    followers_data = cl.user_followers(user_id)
    file_path = os.path.join(target, 'followers.txt')
    with open(file_path, 'w',encoding="utf-8") as fh:
        for i in followers_data:
            #print(f'''Username: "{followers_data[i].username}" Full Name: "{followers_data[i].full_name}" Profile Picture: "{followers_data[i].profile_pic_url}"''')
            fh.write(f'''Username: "{followers_data[i].username}" Full Name: "{followers_data[i].full_name}" Profile Picture: "{followers_data[i].profile_pic_url}"''')
            fh.write('\n')

def user_following(user_id):
    following_data = cl.user_following(user_id)
    file_path = os.path.join(target, 'following.txt')
    with open(file_path, 'w',encoding="utf-8") as fh:
        for i in following_data:
            #print(f'''Username: "{followers_data[i].username}" Full Name: "{followers_data[i].full_name}" Profile Picture: "{followers_data[i].profile_pic_url}"''')
            fh.write(f'''Username: "{following_data[i].username}" Full Name: "{following_data[i].full_name}" Profile Picture: "{following_data[i].profile_pic_url}"''')
            fh.write('\n')

def fetch_images_albums(user_id):
    ## Grabbing all the media that exist on this profile
    unsorted_media = cl.user_medias_v1(user_id)
    sorted_media = media_sorter(unsorted_media)
    return sorted_media

def fetch_videos(user_id):
    unsorted_media = cl.user_clips_v1(user_id)
    sorted_media = media_sorter(unsorted_media)
    return sorted_media

def fetch_tagged(user_id):
    ## Grabbing all the media that exist on this profile
    unsorted_media = cl.usertag_medias_v1(user_id)
    sorted_media = media_sorter(unsorted_media)
    return sorted_media

def combine_media(sorted_photos, sorted_videos):
    final_sort = sorted_photos
    for key in final_sort:
        for values in sorted_videos[key]:
            unique = True
            for j in final_sort[key]:
                if values['id'] == j['id']:
                    unique = False
            if(unique):
                final_sort[key].append(values)
    return final_sort

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

if "session.json" in os.listdir():
    session_file_exists = True
else:
    session_file_exists = False
user_id = False
print('''                                                            
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
                                                            ''')
print('\n\n')
target = input('Please enter your target: ')
clear_screen()
while(True):
    clear_screen()
    print('''                                                            
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
                                                            ''')
    print('\n\n')
    print(f'Current Target is "{target}"\n\n')
    print('Choose one of the following options...')
    print('1. Generate Session File and userid')
    print('2. Summary of target')
    print('3. Find Followers')
    print('4. Find Following')
    print('5. Download All Media')
    print('6. Exit')
    choice = input('Enter Choice: ')
    clear_screen()

    if target not in os.listdir():
        os.mkdir(f"./{target}")

    if "posts" not in os.listdir(target):
        os.mkdir(f"{target}/posts")
    
    media_list = ["images","videos","igtv","reels","albums"]
    for key in media_list:
        if key not in os.listdir(f"{target}/posts"):
            os.mkdir(f"{target}/posts/{key}")

    if not choice.isnumeric():
        print('Invalid choice')
        input('Press Enter to continue...')
        continue

    if not (1<=int(choice)<=6 ):
        print('Invalid choice')
        input('Press Enter to continue...')
        continue

    if(choice == '6'):
        break

    if(choice == '1'):
        if "session.json" not in os.listdir():
            if(generate_session()):
                print('Session file successfully generated')
                session_file_exists = True
                cl = Client()
                cl.delay_range = [3, 10]
                cl.load_settings("session.json")
                input('Press Enter to continue...')
                print('Generating user id... Might take a few seconds. Try your command again after this process is complete')
                user_id = cl.user_id_from_username(target)
                print('User ID Generated')
                input('Press Enter to continue...')
                continue
            else:
                print('Something went wrong, restart the script')
                break
        else:
            print("Session File Already Found, you can continue. If you do not want to use it, please delete the session.json file. And try again.")
            session_file_exists = True
            cl = Client()
            cl.delay_range = [3, 10]
            cl.load_settings("session.json")
            input('Press Enter to continue...')
            print('Generating user id... Might take a few seconds. Try your command again.')
            user_id = cl.user_id_from_username(target)
            print('User ID Generated')
            input('Press Enter to continue...')
            continue
    elif(choice == '2' and session_file_exists):
        user_info = cl.user_info(user_id)
        generate_user_info_file(target, user_info)
        user_summary(user_info)
        input('Press Enter to continue...')
        continue
    elif(choice == '3' and session_file_exists and user_id):
        print('Might take a few minutes depending upon the target, please be patient.')
        user_followers(user_id)
        print('Done!')
        input('Press Enter to continue...')
        continue
    elif(choice == '4' and session_file_exists and user_id):
        print('Might take a few minutes depending upon the target, please be patient.')
        user_following(user_id)
        print('Done!')
        input('Press Enter to continue...')
        continue
    elif(choice == '5' and session_file_exists and user_id):
        print("Fetching all the media, might take a while.")
        final_sort = combine_media(fetch_images_albums(user_id), fetch_videos(user_id))

        with open(f"{target}/posts/media.pickle", "ab") as fh:
            pickle.dump(final_sort, fh)
        with open(f"{target}/posts/media.txt", "w", encoding="utf-8") as outfile: 
            outfile.write(str(final_sort))
        media_downloader(final_sort, target)
        print('Done!')
        input('Press Enter to continue...')
        continue
    else:

        print('Congratulations, you broke the script somehow, contact the main author with screenshots and explanation as to what you did.')

