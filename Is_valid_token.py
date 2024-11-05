import requests

# Replace this with your actual Bearer Token
your_bearer_token = "AAAAAAAAAAAAAAAAAAAAAPaLwgEAAAAAbKsy1txzb6mgC7yNNQGcz06VRqU%3DcPSgCOeFL5aUSZFb02IkMqHPY5MfxPZmnumDVZQ5N86uiQiVeo"

url = "https://api.twitter.com/2/users/me"
headers = {
    "Authorization": f"Bearer {your_bearer_token}"
}

response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
