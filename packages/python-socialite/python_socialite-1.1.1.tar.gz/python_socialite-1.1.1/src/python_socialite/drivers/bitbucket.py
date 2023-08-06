import requests
from python_socialite.drivers.abstract_driver import AbstractDriver
from python_socialite.drivers.abstract_user import abstract_user
from python_socialite.exceptions import BadVerification


class BitbucketProvider(AbstractDriver):
    def __init__(self, config):
        """Initialize Google provider."""
        super().__init__(config)
        self.scopes = config.get("scopes", ["account", "email"])

    @staticmethod
    def provider_name():
        return "bitbucket"

    def get_auth_url(self, state=None):
        url = "https://bitbucket.org/site/oauth2/authorize"
        return self.build_url(url, state)

    def get_token_url(self):
        return "https://bitbucket.org/site/oauth2/access_token"

    def get_token_fields(self, code, state=None):
        fields = {
            "redirect_uri": self.redirect_url,
            "code": code,
            "grant_type": "authorization_code",
        }

        if state is not None:
            fields["state"] = state

        return fields

    def get_token(self, code, state=None, request_type="json"):
        url = self.get_token_url()
        data = self.get_token_fields(code, state)
        response = requests.post(url, data, auth=(self.client_id, self.client_secret))
        token = response.json()
        error = token.get("error")
        if error:
            raise BadVerification(response.text)

        return token

    def get_emails(self, access_token):
        url = "https://api.bitbucket.org/2.0/user/emails"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_user_by_token(self, access_token):
        url = "https://api.bitbucket.org/2.0/user"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        user = response.json()
        emails = self.get_emails(access_token)
        user["emails"] = emails.get("values", [])
        return user

    def map_user_to_dict(self, raw_user):
        user = dict(abstract_user)
        user["id"] = raw_user.get("account_id")
        user["name"] = raw_user.get("display_name")
        user["username"] = raw_user.get("username")
        user["avatar"] = raw_user.get("avatar")
        user["provider"] = BitbucketProvider.provider_name()
        user["raw"] = raw_user

        emails = raw_user.get("emails", [])
        if isinstance(emails, list):
            for item in emails:
                if item["is_primary"]:
                    user["email"] = item["email"]
                    break
        return user
