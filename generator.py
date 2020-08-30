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
    return


def get_random_image():
    return


def get_random_from_list(l):
    index = random.randint(0, len(l) - 1)
    return l[index]


def get_random_int(min, max):
    return random.randint(min, max)



# Main -------------------------------------------------------------------------

def generate_user_accounts(n):
    accounts = []
    for i in range(n):
        display_name, username = get_random_name()
        accounts.append({
            'id'          : get_new_id('user'),
            'displayName' : display_name,
            'username'    : username,
            'dateJoined'  : get_random_date(UNIX_TIME.sub(CURRENT_TIME, 5, 'months'), CURRENT_TIME)
        })
    return accounts


def generate():
    users = generate_user_accounts(args.num_users)

# Run --------------------------------------------------------------------------

if (__name__ == '__main__'):
    generate()
