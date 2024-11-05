import time

async def fetch_user_id(username):
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    user_url = f"https://api.twitter.com/2/users/by/username/{username}"
    user_response = requests.get(user_url, headers=headers)
    
    logging.debug(f"Twitter API response status code: {user_response.status_code}")
    logging.debug(f"Twitter API response headers: {user_response.headers}")
    
    if user_response.status_code == 429:
        reset_time = int(user_response.headers["x-rate-limit-reset"])
        current_time = time.time()
        sleep_time = reset_time - current_time
        logging.info(f"Rate limit hit. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        return await fetch_user_id(username)  # Retry after sleeping
    
    if user_response.status_code == 200:
        user_id = user_response.json().get('data', {}).get('id', None)
        return user_id
    return None
