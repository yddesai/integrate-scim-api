from flask import Flask, redirect, render_template, session
from authlib.integrations.flask_client import OAuth

from config import Config
from auth.providers import get_provider

# Create Flask app
app = Flask(__name__)

# Load configuration
config = Config()
app.config.from_object(config)

# Setup OAuth
oauth = OAuth(app)

# Get the configured IdP provider
idp = get_provider(config.IDP_PROVIDER, oauth, config)

@app.route("/login")
def login():
    return idp.get_login_redirect()

@app.route("/callback", methods=["GET", "POST"])
def callback():
    try:
        token = idp.process_callback()
        session["user"] = token
        return redirect("/")
    except Exception as e:
        print(f"Callback error: {str(e)}")
        return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(idp.get_logout_redirect())

@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get('user'),
        idp_name=config.IDP_PROVIDER
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT) 