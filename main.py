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

#making the folder for target
if target not in os.listdir():
    os.mkdir(f"./{target}")

#fetching target info
user_info = cl.user_info(user_id)

#creating user_info.json file
generate_user_info_file(target, user_info)

#user info basic idea
user_summary(user_info)