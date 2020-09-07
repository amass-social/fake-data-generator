# ==============================================================================
# About: generator.py
# ==============================================================================
# generator.py is responsible for:
#   - randomly generating fake data that can be used by the frontend and backend during development

# Imports ----------------------------------------------------------------------

import sys
import json
import time
import random
import argparse

# Command Line Arguments -------------------------------------------------------

# Define argparse help messages
ARGS = {
    '-u': 'the total number of users that will be created.',
    '-f': 'the name of the output file.'
}

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--num-users', dest='num_users', type=int, default=50,     help=ARGS['-u'])
parser.add_argument('-f', '--filename',  dest='filename',  type=str, action='store', help=ARGS['-f'])
args = parser.parse_args()

FILENAME = args.filename if (args.filename is not None) else "data"

# Hyper Parameters -------------------------------------------------------------

ID_LENGTH    = 12
MIN_FRIENDS  = 4
MAX_FRIENDS  = 10
RATIO_GROUPS = 0.1 # <- the number of groups that are created (as a percentage of total number of users)
MIN_TAGS     = 5
MAX_TAGS     = 10
MIN_POSTS    = 15
MAX_POSTS    = 50
MESSAGE_MIN  = 1
MESSAGE_MAX  = 60

# Constants --------------------------------------------------------------------

VALID_ID_TYPES  = ['user', 'post', 'message', 'group']
POSSIBLE_DIGITS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
CURRENT_TIME    = int(time.time())
UNIX_TIME       = None # <- initialize this in the UnixTime class section

# Imported Constants -----------------------------------------------------------

NAMES = {}
with open('./input/names.json', 'r') as f:
    loaded = json.load(f)
    NAMES['first'] = loaded['first']
    NAMES['last'] = loaded['last']

WORDS = []
with open('./input/lorem_ipsum.json', 'r') as f:
    used_words = {}
    loaded = json.load(f)
    for string in loaded:
        for w in string.split(' '):
            word = w.lower()
            word = word.split(',')[0]
            word = word.split('.')[0]
            if (word not in used_words):
                WORDS.append(word)
                used_words[word] = 1


EMOJIS = []
with open('./input/emoji_definitions.json', 'r') as f:
    for emoji_title, obj in json.load(f).items():
        if ('default' in obj):
            EMOJIS.append(obj['default']['emoji'])


IMAGES = []
with open('./input/lorem_picsum.json', 'r') as f:
    for img in json.load(f):
        IMAGES.append(img['download_url'])


# Class: UnixTime --------------------------------------------------------------
# -> wrapper for making unix time easier to use

class UnixTime():

    def __init__(self):
        return

    # this function converts a value, unit pair into seconds (default for epoch time)
    def convert_to_unix_time(self, value, unit):
        if (unit == "seconds"):
            return value
        if (unit == "minutes"):
            return value * 60
        if (unit == "hours"):
            return value * 60 * 60
        if (unit == "days"):
            return value * 60 * 60 * 24
        if (unit == "weeks"):
            return value * 60 * 60 * 24 * 7
        if (unit == "months"):
            return value * 60 * 60 * 24 * 7 * 4
        if (unit == "years"):
            return value * 60 * 60 * 24 * 7 * 4 * 12

    # returns a timestamp that is value*units after the given unix time
    def add(self, unix_time, value, unit):
        return unix_time + self.convert_to_unix_time(value, unit)

    # returns a timestamp that is value*units before the given unix time
    def sub(self, unix_time, value, unit):
        return unix_time - self.convert_to_unix_time(value, unit)


UNIX_TIME = UnixTime()

# Random Content Functions -----------------------------------------------------

def get_new_id(id_type = ''):
    id = f"{id_type}-" if ((len(id_type) > 0) and (id_type in VALID_ID_TYPES)) else ""
    for i in range(ID_LENGTH):
        digit_index = random.randint(0, len(POSSIBLE_DIGITS) - 1)
        id = f"{id}{POSSIBLE_DIGITS[digit_index]}"
    return id


def get_random_name():
    first_name_index = random.randint(0, len(NAMES['first']) - 1)
    last_name_index = random.randint(0, len(NAMES['last']) - 1)
    display_name = f"{NAMES['first'][first_name_index]} {NAMES['last'][last_name_index]}"
    username = f"the{NAMES['first'][first_name_index]}{NAMES['last'][last_name_index]}"
    return display_name, username


def get_random_date(min_date, max_date = CURRENT_TIME):
    return get_random_int(min_date, max_date)


def get_random_text(min_words, max_words):
    text = ""
    capitalized = True
    limit = get_random_int(min_words, max_words)
    for i in range(limit):
        index = random.randint(0, len(WORDS) - 1)
        new_word = WORDS[index].title() if (capitalized) else WORDS[index]
        if (get_random_int(0, 12) == 11):
            new_word = f"{new_word}."
            capitalized = True
        elif (get_random_int(0, 25) == 23):
            new_word = f"{new_word}?"
            capitalized = True
        elif ((get_random_int(0, 9) == 8) and (i != limit - 1)):
            new_word = f"{new_word},"
            capitalized = False
        else:
            capitalized = False
        text = f"{text} {new_word}"

    # end with punctuation
    if (text[-1] != '.' and text[-1] != '?'):
        text = f"{text}."
    return text


def get_random_emoji():
    return get_random_from_list(EMOJIS)


def get_random_image():
    return get_random_from_list(IMAGES)


def get_random_from_list(l):
    index = random.randint(0, len(l) - 1)
    return l[index]

# given a list, return a randomized sublist
def get_random_sublist(l):
    result = []
    threshold = get_random_int(1, 10)
    for item in l:
        if (get_random_int(1, 10) > threshold):
            result.append(item)
    return result

def get_random_int(min, max):
    return random.randint(min, max)

def get_random_bool():
    return get_random_int(0, 1) == 0

# Main -------------------------------------------------------------------------

# creates n random users and returns them
def generate_user_accounts(n):
    accounts    = []
    account_ids = []
    for i in range(n):
        display_name, username = get_random_name()
        id = get_new_id('user')
        account_ids.append(id)
        accounts.append({
            'id'          : id,
            'photo'       : get_random_image(),
            'displayName' : display_name,
            'username'    : username,
            'dateJoined'  : get_random_date(UNIX_TIME.sub(CURRENT_TIME, 12, 'months'), CURRENT_TIME),
            'email'       : f"{username}@email.com",
            'phone'       : 'blank for now',
            'friends'     : [],
            'groups'      : []
        })
    return accounts, account_ids


def find_group(groups, group_id):
    for group in groups:
        if group['id'] == group_id:
            return group

# creates friend groups for each user
def create_friend_groups(users, user_ids):
    groups, member_lookup = [], {}

    # create the groups
    for i in range(int(RATIO_GROUPS * len(users))):
        id = get_new_id('group')
        members = get_random_sublist(user_ids)
        member_lookup[id] = members
        groups.append({
            'id'     : id,
            'members': members,
            'name'   : get_random_text(1, 4)
        })

    # add groups to user objects
    user_to_groups = {}
    for group in groups:
        for user_id in group['members']:
            user_to_groups.setdefault(user_id, [])
            user_to_groups[user_id].append(group['id'])

    for i in range(len(users)):
        user_id = users[i]['id']
        if (user_id in user_to_groups):
            users[i]['groups'] = user_to_groups[user_id]
    return users, groups, member_lookup


# uses groups to create friend connections between our list of users
def create_friend_connections(users, user_ids, groups, member_lookup):
    for user in users:
        friends = []
        num_friends = get_random_int(MIN_FRIENDS, MAX_FRIENDS)

        # try adding friends from groups
        for group_id in user['groups']:
            for group_member in member_lookup[group_id]:
                if (group_member != user['id']):
                    if (len(friends) < num_friends and get_random_bool() == True):
                        friends.append(group_member)


        # fill out friends from people not in groups
        while(len(friends) < num_friends):
            id = get_random_from_list(user_ids)
            if (id not in friends and id != user['id']):
                friends.append(id)
        user['friends'] = friends
    return users


# creates a lookup table of {user/group-id -> [tags]}
def create_tag_preferences(users, groups):
    lookup = {}
    for list_of_objects in [users, groups]:
        for item in list_of_objects:
            lookup[item['id']] = get_random_text(MIN_TAGS, MAX_TAGS)
    return lookup

def create_reactions(users):
    reactions = []
    for user in users:
        if random.random() > .3:
            reactions.append({"userId": user, "emoji": get_random_emoji()})
    return reactions

def create_post(sender_id, receiver, tag):
    member_ids = []
    receiver_id = '' # either a group or user id

    # check if reciever is a user or group
    if type(receiver) is str: # user
        member_ids = [receiver]
        receiver_id = receiver
    else: #group

        member_ids = receiver['members']
        receiver_id = receiver['id']

    return {
        "id"         : get_new_id("post"),
        "senderId"   : sender_id,
        "receiverId" : receiver_id,
        "title"      : get_random_text(1, 6),
        "dateSent"   : get_random_date(UNIX_TIME.sub(CURRENT_TIME, 12, 'months'), CURRENT_TIME),
        "tags"       : tag,
        "content"    : get_random_image(),
        "type"       : get_random_from_list(["link", "image"]),
        "reactions"  : create_reactions([sender_id] + member_ids)
    }

# creates a list of posts sent between users or groups
def create_posts(users, groups, tag_preferences):
    posts = []
    for user in users:
        for friend in user['friends']:
            for i in range(get_random_int(MIN_POSTS, MAX_POSTS)):
                posts.append(create_post(user['id'], friend, get_random_from_list(tag_preferences[user['id']])))

    for group in groups:
        for member in group['members']:
            for i in range(get_random_int(0, MIN_POSTS)):
                posts.append(create_post(member, group, get_random_from_list(tag_preferences[group['id']])))

    return posts

def create_message(sender_id, post_id):
    return {
        'id': get_new_id('message'),
        'senderId' : sender_id,
        'postId'   : post_id,
        'sent'     : get_random_date(UNIX_TIME.sub(CURRENT_TIME, 12, 'months'), CURRENT_TIME),
        'content'  : get_random_text(MESSAGE_MIN, MESSAGE_MAX),
        'type'     : 'text',
        'reactions': []
    }

def create_responses(user_ids, post_id):
    responses = []
    for user_id in user_ids:
        # create a small, random number of responses for each user
        for _ in range(random.randint(0, 3), 3):
            response = create_message(user_id, post_id)
            responses.append(response)
    return responses


# create messages
def create_messages(users, groups, posts):
    messages = []

    for post in posts:
        # 1) add the "description" messages that are sent at the same time as the post
        message = create_message(post['senderId'], post['id'])
        messages.append(message)

        # 2) get all users that are apart of the post conversation
        user_ids = [post['senderId']]
        if post['receiverId'][0] == 'g':
            group = find_group(groups, post['receiverId'])
            user_ids += group['members']
        else:
            user_ids += [post['receiverId']]

        # 3) create response from post members
        responses = create_responses(user_ids, post['id'])
        messages += responses

    return messages


def generate():

    # 1) create user accounts
    users, user_ids = generate_user_accounts(args.num_users)

    # 2) create groups out of users
    users, groups, member_lookup = create_friend_groups(users, user_ids)

    # 3) use groups to create friend connections between users
    users = create_friend_connections(users, user_ids, groups, member_lookup)

    # 4) create a list of frequently talked about tags for each user or group
    tag_preferences = create_tag_preferences(users, groups)

    # 5) Create posts
    posts = create_posts(users, groups, tag_preferences)

    # 6) create chat messages on posts
    messages = create_messages(users, groups, posts)


    # export results to a file
    to_export = {
        'users'    : users,
        'groups'   : groups,
        'posts'    : posts,
        'messages' : messages
    }
    with open(f"./output/{FILENAME}.json", "w") as f:
        json.dump(to_export, f)
    print(f"exported to {FILENAME}.json")

# Run --------------------------------------------------------------------------

if (__name__ == '__main__'):
    generate()
