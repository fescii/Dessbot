import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def test_bearer_token_permissions():
    url = "https://api.twitter.com/2/tweets?ids=1453489038376136710"  # Example tweet ID
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    print("Status Code:", response.status_code)
    if response.status_code == 200:
        print("Bearer Token has valid permissions.")
        print("Response JSON:", response.json())
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    test_bearer_token_permissions()
