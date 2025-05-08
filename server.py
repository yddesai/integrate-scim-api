import os
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

# Load environment variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Create Flask app
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# Configure session settings
app.config.update(
    SESSION_COOKIE_SECURE=False,  # Set to True in production
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# Auth0 configuration
BASE_URL = "http://localhost:5000"  # Update this in production
AUTH0_CALLBACK_URL = f"{BASE_URL}/callback"
AUTH0_BASE_URL = f"https://{env.get('AUTH0_DOMAIN')}"

# Setup Auth0
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'{AUTH0_BASE_URL}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=AUTH0_CALLBACK_URL
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    try:
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        return redirect("/")
    except Exception as e:
        print(f"Callback error: {str(e)}")
        return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        AUTH0_BASE_URL
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": BASE_URL,
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get('user')
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 5000)) 