"""Main module."""
import inspect
from python_socialite.drivers.abstract_driver import AbstractDriver
from python_socialite.drivers.google import GoogleProvider
from python_socialite.drivers.github import GithubProvider
from python_socialite.drivers.facebook import FacebookProvider
from python_socialite.drivers.microsoft import MicrosoftProvider
from python_socialite.drivers.bitbucket import BitbucketProvider


class OAuthProvider:
    def __init__(self, driver, config):
        """Initialize default provider."""
        self.provider = None

        if inspect.isclass(driver) and issubclass(driver, AbstractDriver):
            provider_name = driver.provider_name()
            print(provider_name)
            credentials = config.get(provider_name)
            self.provider = driver(credentials)
        elif isinstance(driver, str):
            credentials = config.get(driver)
            if driver == "google":
                self.provider = GoogleProvider(credentials)
            elif driver == "github":
                self.provider = GithubProvider(credentials)
            elif driver == "facebook":
                self.provider = FacebookProvider(credentials)
            elif driver == "microsoft":
                self.provider = MicrosoftProvider(credentials)
            elif driver == "bitbucket":
                self.provider = BitbucketProvider(credentials)
        if self.provider is None:
            raise ValueError("Invalid socialite driver")

    def set_scopes(self, scopes):
        self.provider.set_scopes(scopes)
        return self

    def get_auth_url(self, state=None):
        return self.provider.get_auth_url(state)

    def get_token(self, code, state=None):
        return self.provider.get_token(code, state)

    def get_user(self, access_token):
        return self.provider.get_user(access_token)
