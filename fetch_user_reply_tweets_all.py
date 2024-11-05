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

# Event handler for new messages
@telegram_client.on(events.NewMessage(pattern='/start'))
async def handler(event):
    save_chat_id(event.chat_id)
    await event.respond("Welcome! Send me a Twitter username to fetch their latest tweets and replies.")
    print(f"Added chat ID: {event.chat_id}")

@telegram_client.on(events.NewMessage)
async def username_handler(event):
    username = event.message.message.strip().replace('@', '')
    tweets_and_replies = await fetch_tweets_and_replies(username)
    if tweets_and_replies:
        await event.respond(f"Tweets and replies from @{username}:\n\n" + tweets_and_replies)
    else:
        await event.respond(f"Could not fetch tweets and replies for @{username}. Please try again.")

# Send messages to all users
async def send_telegram_message(message):
    chat_ids = get_user_chat_ids()
    print(f"Broadcasting to chat IDs: {chat_ids}")
    for chat_id in list(chat_ids):  # Use a copy of the set
        await telegram_client.send_message(chat_id, message)

async def fetch_username(user_id):
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    url = f"https://api.twitter.com/2/users/{user_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json().get('data', {})
        username = user_data.get('username', 'unknown_user')
        return username
    else:
        logging.error(f"Error fetching username: {response.status_code} {response.text}")
        return 'unknown_user'

async def fetch_tweets(user_id, headers):
    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=10"
    tweets_response = requests.get(tweets_url, headers=headers)
    if tweets_response.status_code == 200:
        tweets = tweets_response.json().get('data', [])
        return tweets
    return []

async def fetch_replies_to_tweet(tweet_id, headers):
    replies_url = f"https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{tweet_id}&tweet.fields=author_id,conversation_id,in_reply_to_user_id"
    replies_response = requests.get(replies_url, headers=headers)
    if replies_response.status_code == 200:
        replies = replies_response.json().get('data', [])
        return replies
    return []

async def fetch_user_replies(user_id, headers):
    user_replies_url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{user_id}&tweet.fields=conversation_id,author_id,in_reply_to_user_id"
    user_replies_response = requests.get(user_replies_url, headers=headers)
    if user_replies_response.status_code == 200:
        user_replies = user_replies_response.json().get('data', [])
        return user_replies
    return []

async def fetch_tweets_and_replies(username):
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    user_url = f"https://api.twitter.com/2/users/by/username/{username}"
    user_response = requests.get(user_url, headers=headers)
    if user_response.status_code == 200:
        user_id = user_response.json().get('data', {}).get('id', None)
        if user_id:
            tweets = await fetch_tweets(user_id, headers)
            user_replies = await fetch_user_replies(user_id, headers)
            messages = []

            tasks = []
            for tweet in tweets:
                messages.append(f"Tweet: {tweet['text']}")
                tasks.append(fetch_replies_to_tweet(tweet['id'], headers))

            replies_results = await asyncio.gather(*tasks)
            for replies in replies_results:
                for reply in replies:
                    messages.append(f"  Reply: {reply['text']}")

            for reply in user_replies:
                messages.append(f"User Reply: {reply['text']}")

            return '\n'.join(messages)
    return None

if __name__ == "__main__":
    telegram_client.run_until_disconnected()
