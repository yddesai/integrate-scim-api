import os
from os import environ as env
from dotenv import find_dotenv, load_dotenv

# Load environment variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

class Config:
    # Application settings
    SECRET_KEY = env.get("APP_SECRET_KEY", "your-secret-key")
    BASE_URL = env.get("BASE_URL", "http://localhost:5000")
    PORT = int(env.get("PORT", 5000))

    # Session settings
    SESSION_COOKIE_SECURE = env.get("SESSION_COOKIE_SECURE", "False").lower() == "true"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # IdP Settings
    IDP_PROVIDER = env.get("IDP_PROVIDER", "auth0").lower()  # Options: 'auth0', 'okta'
    
    # Auth0 Settings
    AUTH0_CLIENT_ID = env.get("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = env.get("AUTH0_CLIENT_SECRET")
    AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
    
    # Okta Settings
    OKTA_CLIENT_ID = env.get("OKTA_CLIENT_ID")
    OKTA_CLIENT_SECRET = env.get("OKTA_CLIENT_SECRET")
    OKTA_DOMAIN = env.get("OKTA_DOMAIN")
    OKTA_ISSUER = env.get("OKTA_ISSUER")

    def __init__(self):
        # Validate required settings based on selected IdP
        if self.IDP_PROVIDER == "auth0":
            required = ["AUTH0_CLIENT_ID", "AUTH0_CLIENT_SECRET", "AUTH0_DOMAIN"]
            for key in required:
                if not getattr(self, key):
                    raise ValueError(f"Missing required Auth0 setting: {key}")
        elif self.IDP_PROVIDER == "okta":
            required = ["OKTA_CLIENT_ID", "OKTA_CLIENT_SECRET", "OKTA_DOMAIN", "OKTA_ISSUER"]
            for key in required:
                if not getattr(self, key):
                    raise ValueError(f"Missing required Okta setting: {key}")

    @property
    def CALLBACK_URL(self):
        return f"{self.BASE_URL}/callback" 