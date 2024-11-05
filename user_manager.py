import json
import os

# Initialize user_chat_ids
user_chat_ids = set()

def load_user_chat_ids():
    global user_chat_ids
    if not os.path.exists('user_chat_ids.json'):
        with open('user_chat_ids.json', 'w') as file:
            json.dump([], file)
    with open('user_chat_ids.json', 'r') as file:
        data = file.read().strip()
        if data:
            user_chat_ids = set(json.loads(data))
        else:
            user_chat_ids = set()

def save_chat_id(chat_id):
    user_chat_ids.add(chat_id)
    with open('user_chat_ids.json', 'w') as file:
        json.dump(list(user_chat_ids), file)

def get_user_chat_ids():
    return user_chat_ids

# Load user chat ids at the start
load_user_chat_ids()
