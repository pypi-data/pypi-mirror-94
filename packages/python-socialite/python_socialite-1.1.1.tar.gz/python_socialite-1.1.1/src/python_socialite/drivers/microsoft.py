import requests
from python_socialite.drivers.abstract_driver import AbstractDriver
from python_socialite.drivers.abstract_user import abstract_user


class MicrosoftProvider(AbstractDriver):
    def __init__(self, config):
        """Initialize Google provider."""
        super().__init__(config)
        self.tenant = config.get("tenant", "common")
        self.scopes = config.get("scopes", ["openid", "email", "profile"])

    def get_auth_url(self, state=None):
        url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/authorize"
        return self.build_url(url, state)

    def get_token_url(self):
        return f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/token"

    def get_token_fields(self, code, state=None):
        fields = super().get_token_fields(code, state)
        fields["grant_type"] = "authorization_code"
        return fields

    def get_user_by_token(self, access_token):
        url = "https://graph.microsoft.com/v1.0/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_token(self, code, state=None, request_type="json"):
        return super().get_token(code, state, request_type="form-data")

    def map_user_to_dict(self, raw_user):
        user = dict(abstract_user)
        user["id"] = raw_user.get("id")
        user["name"] = raw_user.get("displayName")
        user["email"] = raw_user.get("userPrincipalName")
        user["avatar"] = raw_user.get("picture")
        user["provider"] = "microsoft"
        user["raw"] = raw_user
        return user
