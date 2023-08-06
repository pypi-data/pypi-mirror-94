import requests
from python_socialite.drivers.abstract_driver import AbstractDriver
from python_socialite.drivers.abstract_user import abstract_user


class GithubProvider(AbstractDriver):
    def __init__(self, config):
        """Initialize Google provider."""
        super().__init__(config)
        self.scopes = config.get("scopes", ["user:email", "read:user"])

    def get_auth_url(self, state=None):
        url = "https://github.com/login/oauth/authorize"
        return self.build_url(url, state)

    def get_token_url(self):
        return "https://github.com/login/oauth/access_token"

    def get_user_by_token(self, access_token):
        url = "https://api.github.com/user"
        headers = {"Authorization": f"token {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def map_user_to_dict(self, raw_user):
        user = dict(abstract_user)
        username = raw_user.get("login")
        user["id"] = raw_user.get("id")
        user["name"] = raw_user.get("name")
        user["email"] = raw_user.get("email")
        user["avatar"] = raw_user.get("avatar_url")
        user["username"] = username
        user["provider"] = "github"
        user["raw"] = raw_user

        if user["email"] is None:
            user["email"] = f"{username}@users.noreply.github.com"

        return user
