import instaloader
L = instaloader.Instaloader()
USER = input('What is your username?\n')

# Your preferred way of logging in:
try:
		L.load_session_from_file(USER)
except:
		L.interactive_login(USER)

def find_followers(target):

	followers = []
	profile = instaloader.Profile.from_username(L.context, target)
	followers_temp = set(profile.get_followers())
	for people in followers_temp:

				followers.append(people.username)
	return followers

def find_following(target):
	following = []
	profile = instaloader.Profile.from_username(L.context, target)
	following_temp = set(profile.get_followees())
	for people in following_temp:
		following.append(people.username)
	return following

def find_friends(target):
	friends = list(set(find_following(target)) & set(find_followers(target)))
	return friends

target = input('Enter the username of your target: ')
target_following = find_following(target)

#writing it into file
f = open(f"{target}'s following.txt", "a")
for i in target_following:
	f.write(str(i))
	f.write(' \n')
f.close
