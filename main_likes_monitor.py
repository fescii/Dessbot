import logging
import asyncio
import requests
from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
from user_manager import save_chat_id, get_user_chat_ids

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

# Twitter API setup
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
oauth_token = os.getenv('TWITTER_OAUTH_TOKEN')

# Telegram bot setup
telegram_api_id = os.getenv('TELEGRAM_API_ID')
telegram_api_hash = os.getenv('TELEGRAM_API_HASH')
telegram_bot_token = os.getenv('TELEGRAM_ACCESS_TOKEN')

logging.debug(f"Telegram API ID: {telegram_api_id}")
logging.debug(f"Telegram API Hash: {telegram_api_hash}")
logging.debug(f"Telegram Bot Token: {telegram_bot_token}")

telegram_client = TelegramClient('bot', telegram_api_id, telegram_api_hash).start(bot_token=telegram_bot_token)

# Handler for /start command
@telegram_client.on(events.NewMessage(pattern='/start'))
async def handler(event):
    save_chat_id(event.chat_id)
    await event.respond("Welcome! Enter the Twitter username to monitor likes.")
    print(f"Added chat ID: {event.chat_id}")

@telegram_client.on(events.NewMessage)
async def username_handler(event):
    username = event.message.message.strip().replace('@', '')
    await event.respond(f"Monitoring likes for @{username}...")
    asyncio.create_task(monitor_likes(username, event))

# Monitor likes for a user and relay to Telegram
async def monitor_likes(username, event):
    user_id = await fetch_user_id(username)
    last_like_id = None
    while True:
        await fetch_and_relay_likes(user_id, username, last_like_id, event)
        await asyncio.sleep(60)  # Check for updates every 60 seconds

async def fetch_user_id(username):
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    user_url = f"https://api.twitter.com/2/users/by/username/{username}"
    user_response = requests.get(user_url, headers=headers)
    if user_response.status_code == 200:
        user_id = user_response.json().get('data', {}).get('id', None)
        return user_id
    return None

async def fetch_and_relay_likes(user_id, username, last_like_id, event):
    headers = {
        "Authorization": f"Bearer {oauth_token}"
    }
    params = {
        "since_id": last_like_id,
        "max_results": 10
    } if last_like_id else {"max_results": 10}
    likes_url = f"https://api.twitter.com/2/users/{user_id}/liked_tweets"
    likes_response = requests.get(likes_url, headers=headers, params=params)
    if likes_response.status_code == 200:
        likes = likes_response.json().get('data', [])
        if likes:
            for like in likes:
                logging.debug(f"Sending like to Telegram: {like['text']}")
                await event.respond(f"New like from @{username}: {like['text']}")
            last_like_id = likes[0]['id']

if __name__ == "__main__":
    telegram_client.run_until_disconnected()
