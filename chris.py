async def fetch_tweets_and_check_replies(user_id):
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
            await fetch_and_send_replies(tweet["id"])
    else:
        logging.error(f"Error fetching tweets: {response.status_code} {response.text}")

async def main():
    user_id = 1562598218005094400  # User ID for Christo16784414
    while True:
        await fetch_tweets_and_check_replies(user_id)
        await asyncio.sleep(45)  # Sleep for 45 seconds

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    telegram_client.run_until_disconnected()
