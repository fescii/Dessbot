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

# Telegram bot setup
telegram_api_id = os.getenv('TELEGRAM_API_ID')
telegram_api_hash = os.getenv('TELEGRAM_API_HASH')
telegram_bot_token = os.getenv('TELEGRAM_ACCESS_TOKEN')

logging.debug(f"Telegram API ID: {telegram_api_id}")
logging.debug(f"Telegram API Hash: {telegram_api_hash}")
logging.debug(f"Telegram Bot Token: {telegram_bot_token}")

telegram_client = TelegramClient('bot', telegram_api_id, telegram_api_hash).start(bot_token=telegram_bot_token)

# Event handler for new messages
@telegram_client.on(events.NewMessage(pattern='/start'))
async def handler(event):
    save_chat_id(event.chat_id)
    await event.respond("Welcome! You will now receive real-time updates.")
    print(f"Added chat ID: {event.chat_id}")

# Send messages to all users
async def send_telegram_message(message):
    chat_ids = get_user_chat_ids()
    print(f"Broadcasting to chat IDs: {chat_ids}")
    for chat_id in list(chat_ids):  # Use a copy of the set
        await telegram_client.send_message(chat_id, message)

async def fetch_and_send_user_tweets(user_id):
    logging.debug(f"Fetching tweets for user ID: {user_id}")
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=10"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logging.debug(f"Response Data: {response.json()}")
        tweets = response.json().get('data', [])
        if not tweets:
            logging.debug("No tweets found.")
        for tweet in tweets:
            message = f'Tweet ID: {tweet["id"]}: {tweet["text"]}'
            logging.debug(f"Sending message: {message}")
            await send_telegram_message(message)
    else:
        logging.error(f"Error fetching tweets: {response.status_code} {response.text}")

async def main():
    user_ids = ["1562598218005094400"]  # List of user IDs
    while True:
        for user_id in user_ids:
            await fetch_and_send_user_tweets(user_id)
        await asyncio.sleep(15)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    telegram_client.run_until_disconnected()
