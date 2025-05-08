# Multi-Provider Authentication Service

A flexible authentication service that supports multiple Identity Providers (IdPs) including Auth0 and Okta. Built with Flask and Authlib, this service provides a clean, extensible architecture for handling different authentication providers.

## Features

- Support for multiple Identity Providers (currently Auth0 and Okta)
- Easy-to-extend architecture for adding new IdPs
- Secure session handling
- Configurable settings through environment variables
- Clean and modern UI
- Error handling and validation

## Project Structure

```
├── auth/
│   └── providers.py     # IdP provider implementations
├── templates/
│   └── home.html       # Template file
├── config.py           # Configuration settings
├── server.py           # Main application file
├── .env               # Environment variables (create from .env.example)
└── .env.example       # Example environment configuration
```

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install flask authlib python-dotenv
   ```

4. Create your environment file:
   ```bash
   cp .env.example .env
   ```

## Configuration

Edit the `.env` file with your IdP settings. The following variables are available:

### Application Settings
```
APP_SECRET_KEY=your-secret-key-here
BASE_URL=http://localhost:5000
PORT=5000
```

### Session Security Settings
```
SESSION_COOKIE_SECURE=False  # Set to True in production
```

### Identity Provider Selection
```
IDP_PROVIDER=auth0  # Options: auth0, okta
```

### Auth0 Settings (required if using Auth0)
```
AUTH0_CLIENT_ID=your-auth0-client-id
AUTH0_CLIENT_SECRET=your-auth0-client-secret
AUTH0_DOMAIN=your-domain.auth0.com
```

### Okta Settings (required if using Okta)
```
OKTA_CLIENT_ID=your-okta-client-id
OKTA_CLIENT_SECRET=your-okta-client-secret
OKTA_DOMAIN=your-okta-domain.okta.com
OKTA_ISSUER=https://your-okta-domain.okta.com
```

## Running the Application

1. Make sure your virtual environment is activated:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Start the server:
   ```bash
   python server.py
   ```

The application will be available at `http://localhost:5000` (or whatever port you configured).

## IdP-Specific Setup

### Auth0 Setup

1. Create a new application in Auth0 Dashboard
2. Configure the following settings:
   - Allowed Callback URLs: `http://localhost:5000/callback`
   - Allowed Logout URLs: `http://localhost:5000`
   - Allowed Web Origins: `http://localhost:5000`
3. Copy the Client ID, Client Secret, and Domain to your `.env` file

### Okta Setup

1. Create a new application in Okta Developer Console
2. Configure the following settings:
   - Sign-in redirect URIs: `http://localhost:5000/callback`
   - Sign-out redirect URIs: `http://localhost:5000`
   - Base URIs: `http://localhost:5000`
3. Copy the Client ID, Client Secret, Domain, and Issuer to your `.env` file

## Adding a New Identity Provider

To add support for a new Identity Provider:

1. Add the provider's configuration settings to `config.py`
2. Create a new provider class in `auth/providers.py` that extends `IdPProvider`
3. Implement the required methods:
   - `setup()`
   - `get_login_redirect()`
   - `get_logout_redirect()`
   - `process_callback()`
4. Add the new provider to the `providers` dictionary in the `get_provider` function

Example of adding a new provider:

```python
class NewProvider(IdPProvider):
    def setup(self):
        self.oauth.register(
            "new_provider",
            client_id=self.config.NEW_PROVIDER_CLIENT_ID,
            client_secret=self.config.NEW_PROVIDER_CLIENT_SECRET,
            # ... additional configuration
        )

    def get_login_redirect(self):
        return self.oauth.new_provider.authorize_redirect(
            redirect_uri=self.config.CALLBACK_URL
        )

    # ... implement other required methods
```
