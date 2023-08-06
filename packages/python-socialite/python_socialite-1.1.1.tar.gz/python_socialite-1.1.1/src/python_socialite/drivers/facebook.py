import requests
from urllib import parse
from python_socialite.drivers.abstract_driver import AbstractDriver
from python_socialite.drivers.abstract_user import abstract_user
from python_socialite.exceptions import BadVerification


class FacebookProvider(AbstractDriver):
    def __init__(self, config):
        """Initialize Google provider."""
        super().__init__(config)
        fb_scopes = ["email", "public_profile"]
        self.scopes = config.get("scopes", fb_scopes)

    def get_auth_url(self, state=None):
        url = "https://www.facebook.com/v9.0/dialog/oauth"
        return self.build_url(url, state)

    def get_token_url(self):
        return "https://graph.facebook.com/v9.0/oauth/access_token"

    def get_token_fields(self, code, state=None):
        fields = super().get_token_fields(code, state)
        fields["grant_type"] = "authorization_code"
        return fields

    def get_user_by_token(self, access_token):
        url = "https://graph.facebook.com/v9.0/me"
        url = url + "?fields=name,email,id,picture,first_name,last_name"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def build_token_url(self, code, state=None):
        url = self.get_token_url()
        fields = self.get_token_fields(code, state)
        parts = list(parse.urlparse(url))
        query = dict(parse.parse_qsl(parts[4]))
        query.update(fields)
        parts[4] = parse.urlencode(query, quote_via=parse.quote)
        return parse.urlunparse(parts)

    def get_token(self, code, state=None, request_type="json"):
        url = self.build_token_url(code, state)
        response = requests.get(url)
        token = response.json()
        error = token.get("error")
        if error:
            raise BadVerification(response.text)
        return token

    def map_user_to_dict(self, raw_user):
        user_id = raw_user.get("id")
        avatar_url = (
            f"https://graph.facebook.com/v9.0/{user_id}/picture/?type=large&width=1600"
        )
        user = dict(abstract_user)
        user["id"] = user_id
        user["name"] = raw_user.get("name")
        user["email"] = raw_user.get("email")

        # access to avatar requires a valid access_token
        user["avatar"] = avatar_url
        user["provider"] = "facebook"
        user["raw"] = raw_user
        return user
