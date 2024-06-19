from utils import generate_session
from utils import generate_user_info_file
from utils import user_summary
from instagrapi import Client
import os

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

target = input('Please enter your target: ')
clear_screen()
while(True):
    clear_screen()
    print(f'Current Target is "{target}"\n\n')
    print('Choose one of the following options...')
    print('1. Generate Session File')
    print('2. Summary of target')
    print('3. Find Followers')
    print('4. Find Following')
    print('5. Exit')
    choice = input('Enter Choice: ')
    clear_screen()
    if target not in os.listdir():
        os.mkdir(f"./{target}")
    if not choice.isnumeric():
        print('Invalid choice')
        input('Press Enter to continue...')
        continue

    if not (1<=int(choice)<=5 ):
        print('Invalid choice')
        input('Press Enter to continue...')
        continue

    if(choice == '5'):
        break

    if(choice == '1'):
        if "session.json" not in os.listdir():
            if(generate_session()):
                print('Session file successfully generated')
                session_file_exists = True
                cl = Client()
                cl.delay_range = [1, 10]
                cl.load_settings("session.json")
                input('Press Enter to continue...')
                print('Generating user id... Might take a few seconds. Try your command again.')
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
            cl.delay_range = [1, 10]
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
    elif(choice == '3' and session_file_exists):
        print('Might take a few minutes depending upon the target, please be patient.')
        user_followers(user_id)
        print('Done!')
        input('Press Enter to continue...')
        continue
    elif(choice == '4' and session_file_exists):
        print('Might take a few minutes depending upon the target, please be patient.')
        user_following(user_id)
        print('Done!')
        input('Press Enter to continue...')
        continue
    else:
        print('Congratulations, you broke the script somehow, contact the main author with screenshots and explanation as to what you did.')

