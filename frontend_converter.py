# ==============================================================================
# About: frontend_converter.py
# ==============================================================================
# frontend_converter.py is responsible for:
#   - converting output from generator.py into a format that is usable by the frontend
#   - This means:
#       - filtering through the data to focus on one user account

# Imports ----------------------------------------------------------------------

import sys
import json
import argparse

# Main -------------------------------------------------------------------------

# returns a lookup of all users {userid -> user object}
def get_all_users_lookup(data):
    lookup = {}
    for user in data['users']:
        lookup[user['id']] = user
    return lookup

# returns a lookup of all {postId -> [message objects]}
def get_post_to_messages_lookup(data):
    lookup = {}
    for message in data['messages']:
        if (message['postId'] not in lookup):
            lookup[message['postId']] = []
        lookup[message['postId']].append(message)
    return lookup


# main function
def convert(data):

    all_users_lookup = get_all_users_lookup(data)
    post_to_messages = get_post_to_messages_lookup(data)

    # 1) build up this user
    main_user = data['users'][0]
    user_id = main_user['id']
    obj_lookup = {} # {id->object}
    ids = {
        'friends'       : [],
        'users'         : [],
        'groups'        : [],
        'postsSent'     : [],
        'postsReceived' : []
    }

    # get account info for all the user's friends
    for friend_id in main_user['friends']:
        obj_lookup[friend_id] = all_users_lookup[friend_id]
        ids['friends'].append(friend_id)
        ids['users'].append(friend_id)


    # get groups that our user is a part of
    #   -> add account info for any user that is in a group with our main user
    for group in data['groups']:
        if (user_id in group['members']):
            group_id = group['id']
            obj_lookup[group_id] = group
            ids['groups'].append(group_id)

            for member_id in group['members']:
                if (member_id not in obj_lookup):
                    obj_lookup[member_id] = all_users_lookup[member_id]
                    ids['users'].append(member_id)


    # get posts + messages!
    for post in data['posts']:
        post_id = post['id']
        if (post['senderId'] == user_id):

            obj_lookup[post_id] = post
            message_ids = []
            for message in post_to_messages[post_id]:
                obj_lookup[message['id']] = message
                message_ids.append(message['id'])
            ids['postsSent'].append({
                'id'      : post_id,
                'chat'    : message_ids
            })

        if (post['receiverId'] == user_id):
            obj_lookup[post_id] = post
            message_ids = []
            for message in post_to_messages[post_id]:
                obj_lookup[message['id']] = message
                message_ids.append(message['id'])
            ids['postsReceived'].append({
                'id'      : post_id,
                'chat'    : message_ids
            })
    return {
        'user'  : main_user,
        'lookup': obj_lookup,
        'groups': ids
    }


# Argparse ---------------------------------------------------------------------

ARGS = {
    '-i': 'The name of the input file, located at /output/{filename}. Do not include the filetype.',
    '-o': 'The name of the output file that this program will write to. Do not include the filetype'
}
# Parse args
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-filename',  dest='input_filename',  type=str, default="data",          help=ARGS['-i'])
parser.add_argument('-o', '--output-filename', dest='output_filename', type=str, default="frontend-data", help=ARGS['-o'])
args = parser.parse_args()

# Run --------------------------------------------------------------------------

if (__name__ == '__main__'):
    data = {}
    with open(f'./output/{args.input_filename}.json', 'r') as f:
        data = json.load(f)
    to_export = convert(data)
    with open(f"./output/{args.output_filename}.json", "w") as f:
        json.dump(to_export, f)
