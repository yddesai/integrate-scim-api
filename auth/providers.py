from abc import ABC, abstractmethod
from urllib.parse import quote_plus, urlencode

class IdPProvider(ABC):
    def __init__(self, oauth, config):
        self.oauth = oauth
        self.config = config
        self.setup()

    @abstractmethod
    def setup(self):
        """Configure the OAuth client for this provider"""
        pass

    @abstractmethod
    def get_login_redirect(self):
        """Get the login redirect URL"""
        pass

    @abstractmethod
    def get_logout_redirect(self):
        """Get the logout redirect URL"""
        pass

    @abstractmethod
    def process_callback(self):
        """Process the callback from the IdP"""
        pass

class Auth0Provider(IdPProvider):
    def setup(self):
        self.oauth.register(
            "auth0",
            client_id=self.config.AUTH0_CLIENT_ID,
            client_secret=self.config.AUTH0_CLIENT_SECRET,
            client_kwargs={
                "scope": "openid profile email",
            },
            server_metadata_url=f'https://{self.config.AUTH0_DOMAIN}/.well-known/openid-configuration'
        )

    def get_login_redirect(self):
        return self.oauth.auth0.authorize_redirect(
            redirect_uri=self.config.CALLBACK_URL
        )

    def get_logout_redirect(self):
        return f"https://{self.config.AUTH0_DOMAIN}/v2/logout?" + urlencode(
            {
                "returnTo": self.config.BASE_URL,
                "client_id": self.config.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )

    def process_callback(self):
        return self.oauth.auth0.authorize_access_token()

class OktaProvider(IdPProvider):
    def setup(self):
        self.oauth.register(
            "okta",
            client_id=self.config.OKTA_CLIENT_ID,
            client_secret=self.config.OKTA_CLIENT_SECRET,
            client_kwargs={
                "scope": "openid profile email"
            },
            server_metadata_url=f'{self.config.OKTA_ISSUER}/.well-known/openid-configuration'
        )

    def get_login_redirect(self):
        return self.oauth.okta.authorize_redirect(
            redirect_uri=self.config.CALLBACK_URL
        )

    def get_logout_redirect(self):
        return f"{self.config.OKTA_ISSUER}/v1/logout?" + urlencode(
            {
                "post_logout_redirect_uri": self.config.BASE_URL,
                "client_id": self.config.OKTA_CLIENT_ID,
            },
            quote_via=quote_plus,
        )

    def process_callback(self):
        return self.oauth.okta.authorize_access_token()

def get_provider(provider_name, oauth, config):
    providers = {
        "auth0": Auth0Provider,
        "okta": OktaProvider
    }
    
    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Unsupported IdP provider: {provider_name}")
    
    return provider_class(oauth, config) 