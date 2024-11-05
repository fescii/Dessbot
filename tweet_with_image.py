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

async def fetch_and_send_tweet_with_image(tweet_id):
    logging.debug(f"Fetching tweet with ID: {tweet_id}")
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    url = f"https://api.twitter.com/2/tweets/{tweet_id}?expansions=attachments.media_keys&media.fields=url"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tweet = response.json().get('data', {})
        includes = response.json().get('includes', {}).get('media', [])
        if tweet:
            message = f'Tweet ID: {tweet["id"]}: {tweet["text"]}'
            for media in includes:
                if media.get('type') == 'photo':
                    message += f'\nImage: {media["url"]}'
            logging.debug(f"Sending message: {message}")
            await send_telegram_message(message)
        else:
            logging.debug("No tweet found.")
    else:
        logging.error(f"Error fetching tweet: {response.status_code} {response.text}")

if __name__ == "__main__":
    # Example tweet IDs to lookup
    tweet_ids = [
        "1562598218005094400"
    ]

    loop = asyncio.get_event_loop()
    for tweet_id in tweet_ids:
        loop.run_until_complete(fetch_and_send_tweet_with_image(tweet_id))

    telegram_client.run_until_disconnected()
