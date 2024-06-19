from utils import generate_session
from utils import generate_user_info_file
from utils import user_summary
from instagrapi import Client
import os

if "session.json" not in os.listdir():
    generate_session()
else:
    print("Session File Found, you can continue")

cl = Client()
cl.delay_range = [1, 10]
cl.load_settings("session.json")

target = input("Enter your target username: ")
user_id = cl.user_id_from_username(target)

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

#making the folder for target
if target not in os.listdir():
    os.mkdir(f"./{target}")

#fetching target info
user_info = cl.user_info(user_id)

#creating user_info.json file
generate_user_info_file(target, user_info)

#user info basic idea
user_summary(user_info)

#user followers
user_followers(user_id)

#user following
user_following(user_id)

