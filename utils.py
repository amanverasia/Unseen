from instagrapi import Client
import requests
import os

def generate_session():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    otp_from_totp = input("Enter your OTP: ")
    cl = Client()
    cl.delay_range = [1, 10]
    try:
        cl.login(username, password, False, otp_from_totp)
        cl.dump_settings("session.json")
        return True
    except Exception as e:
        print(e)
        return False


def generate_user_info_file(target, user_info):
    file_path = os.path.join(target, 'user_info.json')
    with open(file_path, "w",encoding="utf-8") as fh:
        fh.write("{")
        for index, i in enumerate(list(user_info)):
            fh.write(f'''"{i[0]}": ''')
            fh.write('"')
            fh.write(str(i[1]).replace('\n',''))
            fh.write('"')
            if index < len(list(user_info))-1:
                fh.write(',\n')
        fh.write("}")
    file_path = os.path.join(target, f'{target}.jpg')
    url = user_info.profile_pic_url_hd
    data = requests.get(url).content 
    f = open(file_path,'wb',) 
    f.write(data) 
    f.close() 

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


def media_sorter(media):
    images = [] #media_type=1
    videos = [] #media_type=2 and product_type=feed
    igtv = [] #media_type=2 and product_type=igtv
    reels = [] #When media_type=2 and product_type=clips
    albums = [] #media_type=8

    for i in media:
        #for images
        if (i.media_type == 1):
            images.append({"id":i.id, 
                        "code":i.code, 
                        "taken_time":i.taken_at.strftime("%d-%m-%Y %H:%M:%S %Z"), 
                        "url": i.thumbnail_url, 
                        "likes":i.like_count, 
                        "comment_count":i.comment_count, 
                        "caption":i.caption_text})
        
        #for videos
        if(i.media_type == 2 and i.product_type == "feed"):
            videos.append({"id":i.id, 
                        "code":i.code, 
                        "taken_time":i.taken_at.strftime("%d-%m-%Y %H:%M:%S %Z"),
                        "url":i.video_url,
                        "likes":i.like_count, 
                        "comment_count":i.comment_count, 
                        "caption":i.caption_text,
                        "view_count":i.view_count})
            
        #for igtv
        if(i.media_type == 2 and i.product_type == "igtv"):
            igtv.append({"id":i.id, 
                        "code":i.code, 
                        "taken_time":i.taken_at.strftime("%d-%m-%Y %H:%M:%S %Z"),
                        "url":i.video_url,
                        "likes":i.like_count, 
                        "comment_count":i.comment_count, 
                        "caption":i.caption_text,
                        "view_count":i.view_count})

        #for reels    
        if(i.media_type == 2 and i.product_type == "clips"):
            reels.append({"id":i.id, 
                        "code":i.code, 
                        "taken_time":i.taken_at.strftime("%d-%m-%Y %H:%M:%S %Z"),
                        "url":i.video_url,
                        "thumbnail_url": i.thumbnail_url,
                        "likes":i.like_count, 
                        "comment_count":i.comment_count, 
                        "caption":i.caption_text,
                        "view_count":i.play_count})

        #for albums    
        if(i.media_type == 8):
            album_resource_urls = []
            for j in i.resources:
                if j.media_type == 1:
                    album_resource_urls.append(j.thumbnail_url)
                if j.media_type == 2:
                    album_resource_urls.append(j.video_url)
            albums.append({"id":i.id, 
                        "code":i.code, 
                        "taken_time":i.taken_at.strftime("%d-%m-%Y %H:%M:%S %Z"),
                        "urls": album_resource_urls,
                        "likes":i.like_count, 
                        "comment_count":i.comment_count, 
                        "caption":i.caption_text,
                        })
    return {
        "images": images,
        "videos": videos,
        "igtv": igtv,
        "reels": reels,
        "albums": albums
    }

def media_downloader(final_sort, target):
    for key in final_sort:
        print(f"Working for {key}")
        count = 0
        for i in final_sort[key]:
            print(i)
            if(key == "images"):
                file_path = os.path.join(f'{target}/posts/{key}', f'{i["id"]}.jpg')
                url = i['url']
                data = requests.get(url).content 
                f = open(file_path,'wb',) 
                f.write(data) 
                f.close()        
            if (key == "igtv" or key == "videos" or key == "reels"):
                file_path = os.path.join(f'{target}/posts/{key}', f'{i["id"]}.mp4')
                url = i['url']
                data = requests.get(url).content 
                f = open(file_path,'wb',) 
                f.write(data) 
                f.close()
            if(key == "albums"):
                if i["id"] not in os.listdir("{target}/posts/albums"):
                    os.mkdir(f"{target}/posts/albums/{i['id']}")
                for url in i["urls"]:
                    count += 1
                    file_path = os.path.join(f'{target}/posts/albums/{i["id"]}', f'{count} {i["id"]}.jpg')
                    data = requests.get(url).content 
                    f = open(file_path,'wb',) 
                    f.write(data) 
                    f.close()