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
    '-u': 'the total number of users that will be created.'
}

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--num-users', dest='num_users', type=int, default=30, help=ARGS['-u'])
args = parser.parse_args()


# Hyper Parameters -------------------------------------------------------------

ID_LENGTH = 12

# Constants --------------------------------------------------------------------

VALID_ID_TYPES = ['user', 'post', 'chat', 'message', 'group']
POSSIBLE_DIGITS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"

# Imported Constants -----------------------------------------------------------

NAMES = {}
with open('./input/names.json', 'r') as f:
    loaded = json.load(f)
    NAMES['first'] = loaded['first']
    NAMES['last'] = loaded['last']


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


def get_random_date():
    return


# Main -------------------------------------------------------------------------

def generate_user_accounts(n):
    accounts = []
    for i in range(n):
        display_name, username = get_random_name()
        accounts.append({
            'id'          : get_new_id('user'),
            'displayName' : display_name,
            'username'    : username
        })
    return accounts


def generate():
    users = generate_user_accounts(args.num_users)

# Run --------------------------------------------------------------------------

if (__name__ == '__main__'):
    generate()
