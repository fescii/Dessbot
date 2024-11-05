from flask import Flask, redirect, request, session
import random
import string
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret")  # Ensure to set a secret key

#this is hard bro,hehehe
# Function to generate a random string for the state parameter
def generate_random_string(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/login')
def login():
    client_id = os.environ.get("TWITTER_CLIENT_ID")  # Use environment variable for Client ID
    redirect_uri = os.environ.get("TWITTER_REDIRECT_URI", "https://example.com/callback")
    state = generate_random_string()  # Generate a secure random string
    code_challenge = os.environ.get("CODE_CHALLENGE", "u90Q8sVvOYOfZjkvZLgtNVWQBAWnqnVRPx-lWTvir6k")

    # Store the state in the session for validation later
    session['oauth_state'] = state

    authorization_url = (
        f"https://twitter.com/i/oauth2/authorize?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"scope=tweet.read%20users.read&"
        f"state={state}&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256"
    )
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')

    # Validate the state parameter
    if state != session.get('oauth_state'):
        return "State parameter does not match.", 400

    # Exchange the authorization code for an access token
    access_token = exchange_code_for_access_token(code)
    if access_token:
        session['access_token'] = access_token  # Store access token in session
        return "Access Token received! You can now use it to access user info."
    return "Failed to obtain access token.", 400

def exchange_code_for_access_token(code):
    url = "https://api.twitter.com/2/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "client_id": os.environ.get("TWITTER_CLIENT_ID"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.environ.get("TWITTER_REDIRECT_URI", "https://example.com/callback"),
        "code_verifier": os.environ.get("CODE_VERIFIER", "JrcCV94yLsN4pRBcI2U3UDiimn4FFlRTlGhRW5oO8bQ")
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Error exchanging code for access token:", response.json())
        return None

@app.route('/me')
def get_user():
    access_token = session.get("access_token")  # Retrieve access token from session
    if not access_token:
        return "No access token found. Please log in again.", 403

    url = "https://api.twitter.com/2/users/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return f"User Info: {response.json()}"
    return "Error fetching user info.", 400

if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for development
