import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if variables are loaded
print("TWITTER_BEARER_TOKEN:", os.getenv('TWITTER_BEARER_TOKEN'))
print("TWITTER_API_KEY:", os.getenv('TWITTER_API_KEY'))
print("TWITTER_API_KEY_SECRET:", os.getenv('TWITTER_API_KEY_SECRET'))
print("TWITTER_ACCESS_TOKEN:", os.getenv('TWITTER_ACCESS_TOKEN'))
print("TWITTER_ACCESS_SECRET:", os.getenv('TWITTER_ACCESS_SECRET'))
print("TELEGRAM_API_ID:", os.getenv('TELEGRAM_API_ID'))
print("TELEGRAM_API_HASH:", os.getenv('TELEGRAM_API_HASH'))
print("TELEGRAM_ACCESS_TOKEN:", os.getenv('TELEGRAM_ACCESS_TOKEN'))
print("TELEGRAM_CHAT_ID:", os.getenv('TELEGRAM_CHAT_ID'))
