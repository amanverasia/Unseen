import instaloader
import networkx as nx
import matplotlib.pyplot as plt

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

target1 = input('Enter the username of your target1: ')
target2 = input('Enter the username of your target2: ')

target1_followers = find_followers(target1)
target2_followers = find_followers(target2)

common = list(set(target1_followers) & set(target2_followers))

# print(target1_followers)
# print(target2_followers)

#writing it into file
f = open(f"{target1}'s followers.txt", "a")
for i in target1_followers:
	f.write(str(i))
	f.write(' \n')
f.close

f = open(f"{target2}'s followers.txt", "a")
for i in target2_followers:
	f.write(str(i))
	f.write(' \n')
f.close

f = open("common followers.txt", "a")
for i in common:
	f.write(str(i))
	f.write(' \n')
f.close

G = nx.Graph()

edges = [ ]
for words in common:
  edges.append((target1, words))
G.add_edges_from(edges)

for words in common:
  edges.append((target2, words))
G.add_edges_from(edges)

plt.figure(1,figsize=(10,10))
nx.draw_spring(G,node_color='cyan', node_size=600,font_size=8, with_labels=True)
plt.savefig("common_followers.png") # save as png
plt.show() # display