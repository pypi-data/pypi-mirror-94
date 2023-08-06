"""Main module."""
from python_socialite.drivers.google import GoogleProvider
from python_socialite.drivers.github import GithubProvider
from python_socialite.drivers.facebook import FacebookProvider
from python_socialite.drivers.microsoft import MicrosoftProvider


class OAuthProvider:
    def __init__(self, driver, config):
        """Initialize default provider."""

        credentials = config.get(driver)

        if driver == "google":
            self.provider = GoogleProvider(credentials)
        elif driver == "github":
            self.provider = GithubProvider(credentials)
        elif driver == "facebook":
            self.provider = FacebookProvider(credentials)
        elif driver == "microsoft":
            self.provider = MicrosoftProvider(credentials)
        else:
            raise ValueError("Invalid socialite driver")

    def set_scopes(self, scopes):
        self.provider.set_scopes(scopes)
        return self

    def get_auth_url(self, state=None):
        return self.provider.get_auth_url(state)

    def get_token(self, code, state=None, type="json"):
        return self.provider.get_token(code, state, type)

    def get_user(self, access_token):
        return self.provider.get_user(access_token)
