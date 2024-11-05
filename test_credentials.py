import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set your credentials
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

def test_credentials():
    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

    response = requests.get(url, auth=auth)

    print("Status Code:", response.status_code)
    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    test_credentials()
