from instagrapi import Client
import os

def generate_session():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    otp_from_totp = input("Enter your OTP: ")
    cl = Client()
    cl.delay_range = [1, 10]
    cl.login(username, password, False, otp_from_totp)
    cl.dump_settings("session.json")
    return "Success"

def generate_user_info_file(target, user_info):
    file_path = os.path.join(target, 'user_info.json')
    with open(file_path, "w") as fh:
        fh.write("{")

        for index, i in enumerate(list(user_info)):
            fh.write(f'''"{i[0]}": ''')
            fh.write('"')
            fh.write(str(i[1]).replace('\n',''))
            fh.write('"')
            if index < len(list(user_info))-1:
                fh.write(',\n')
        fh.write("}")

def user_summary(user_info):
    print(f"Summary for '{user_info.username}'")
    print("--------------------------------")
    print(f"Target has full name/nickname set to '{user_info.full_name}' and has {user_info.follower_count} followers, {user_info.following_count} folowing and a media count of {user_info.media_count}.")
    print(f"The Instagram Bio is set to,")
    print("```")
    print(str(user_info.biography))
    print("```")
    print("--------------------------------")
    print()
    print(f"More information can be found inside the {user_info.username}/user_info.json file.")