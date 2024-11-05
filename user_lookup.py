import logging
import asyncio
import requests
from telethon import TelegramClient
import os
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

# Twitter API setup
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

# Telegram bot setup
telegram_api_id = os.getenv('TELEGRAM_API_ID')
telegram_api_hash = os.getenv('TELEGRAM_API_HASH')
telegram_bot_token = os.getenv('TELEGRAM_ACCESS_TOKEN')
telegram_chat_id = int(os.getenv('TELEGRAM_CHAT_ID'))  # Ensure it is an integer

logging.debug(f"Telegram API ID: {telegram_api_id}")
logging.debug(f"Telegram API Hash: {telegram_api_hash}")
logging.debug(f"Telegram Bot Token: {telegram_bot_token}")
logging.debug(f"Telegram Chat ID: {telegram_chat_id}")

telegram_client = TelegramClient('bot', telegram_api_id, telegram_api_hash).start(bot_token=telegram_bot_token)

async def send_telegram_message(message):
    await telegram_client.send_message(telegram_chat_id, message)

async def fetch_and_send_user_info(username):
    logging.debug(f"Fetching user info for: {username}")
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user = response.json().get('data', {})
        if user:
            message = f'User Info: Username: {user["username"]}, Name: {user["name"]}, ID: {user["id"]}'
            logging.debug(f"Sending message: {message}")
            await send_telegram_message(message)
        else:
            logging.debug("No user found.")
    else:
        logging.error(f"Error fetching user info: {response.status_code} {response.text}")

if __name__ == "__main__":
    # Example usernames to lookup
    usernames = [
        "ooko_clinton",  # Replace with actual usernames you want to lookup
        
    ]

    loop = asyncio.get_event_loop()
    for username in usernames:
        loop.run_until_complete(fetch_and_send_user_info(username))

    telegram_client.run_until_disconnected()
