# python-socialite
<p align="center">

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/277f72118617436291eced30bac036a8)](https://www.codacy.com/manual/evans.mwendwa/python-socialite?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=evansmwendwa/python-socialite&amp;utm_campaign=Badge_Grade)
<a href="https://pypi.python.org/pypi/python_socialite">
<img src="https://img.shields.io/pypi/v/python_socialite.svg" /></a>
<a href=""><img src="https://github.com/evansmwendwa/python-socialite/workflows/build/badge.svg" /></a> [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/277f72118617436291eced30bac036a8)](https://www.codacy.com/manual/evans.mwendwa/python-socialite?utm_source=github.com&utm_medium=referral&utm_content=evansmwendwa/python-socialite&utm_campaign=Badge_Coverage)

</p>

<img src="https://raw.githubusercontent.com/evansmwendwa/python-socialite/master/banner.png" alt="" />

## The easy way to retrieve OAuth 2.0 Tokens from any provider

Simple and convenient way for fetching OAuth 2.0 tokens from any provider. Out of the box support for Facebook, Twitter, LinkedIn, Google, GitHub, GitLab and Bitbucket. Inspired by [Laravel Socialite](https://laravel.com/docs/master/socialite)

## Features
-   Supports multiple common providers
-   Supports any oAuth 2 compliant providers (You can provide a custom driver)
-   Straighforward unopinionated authentication
-   Can be implemented in any python framework

## Usage

### Installation

```shell
pip install python-socialite
```

### Generate redirect uri
```python
from python_socialite import OAuthProvider

config = {
    "google": {
        "client_id": "",
        "client_secret": "",
        "redirect_url": ""
    }
}
provider = OAuthProvider("google", config)
redirect_url = provider.get_auth_url()

# redirect user to the redirect_url using your frameworks supported redirect
```

### Retrieving Access Token and User

```python
code = "" # read code from GET variables in the url the provider redirected you to
provider = OAuthProvider("google", config)

token = provider.get_token(code)
user = provider.get_user(token["access_token"])
```

This package does not provide opinion on how you use the returned token or user profile. Add that to your application's business logic. Examples include hooking up to your authentication logic, fetching data associated with the returned access token e.t.c

### Token Template

**NB:** Token attributes might vary between providers. Here's a sample returned by Google oAuth

```json
{
   "access_token": "ya29.***",
   "expires_in": 3599,
   "scope": "https://www.googleapis.com/auth/userinfo.profile openid",
   "token_type": "Bearer",
   "id_token": "***jwt***"
}
```

### User Template

```python
user = {
    "id": "",
    "name": "",
    "email": "",
    "avatar": "",
    "raw": "",
    "provider": ""
}
```

The `raw` attribute contains all user data as returned by the oAuth provider. Fields in this attribute can be different across different oAuth providers

### Requesting Scopes

By default the following scopes are requested

```shell
openid, email, profile
```

You can override requested scopes by adding them to the provider config or using `set_scopes` method

```python
provider = OAuthProvider("google", config)
auth_url = provider.set_scopes(["openid", "email", "profile"]).get_auth_url()
```
**NB:** *If no scopes are set in the config or in code the default scopes will be used*

### Config Options

The config must be a dict containing keys of any of the supported providers

```python
# each provider key must have client_id, client_secret and redirect_url. It's advised to ensure your client_secret is properly secured

config = {
    "google": {
        "client_id": "",
        "client_secret": "",
        "redirect_url": "",
        "scopes": [] # optional
    },
    "facebook": {},
    "twitter": {},
    "linkedin": {},
    "github": {},
    "gitlab": {},
    "bitbucket": {}
}

```
