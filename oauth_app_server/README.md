
An OAuth app server for testing, supports GitHub and Facebook.  


## Pre-requisites
Before running, we need to setup the OAuth app on the provider's side.  

### GitHub App
Go to [GitHub Developer Settings](https://github.com/settings/developers) and create a new OAuth app.  

Set the following fields:
- `Application name`: `OAuth App Server`
- `Homepage URL`: `http://localhost:1338/`
- `Authorization callback URL`: `http://localhost:1338/github-callback`

After creating the app, copy the `Client ID` and `Client Secret` to the `github_oauth_config` array. 
Here is an example:  
```python
github_oauth_config = {
    "client_id": "<client_id>",
    "client_secret": "<client_secret>",
    "scopes": ["<scope>"],
    "auth_url": "https://github.com/login/oauth/authorize",
    "token_url": "https://github.com/login/oauth/access_token",
    "redirect_url": f"http://localhost:{PORT}/github-callback",
}  
```
### Facebook App
Go to [Facebook Developer](https://developers.facebook.com/apps/) and create a new app.  

Set the following fields:
- `Display name`: `MyCoolApp`
- `Site URL`: `http://localhost:1338/facebook-callback
- `Privacy Policy URL`: `https://example.com/`
- `Authorization callback URL`: `http://localhost:1338/github-callback`

After creating the app, copy the `Client ID` and `Client Secret` to the `facebook_oauth_config` array.  

Here is an example:  
```python
facebook_oauth_config = {
    # MyCoolApp - victim1338
    "client_id": "<client_id>",
    "client_secret": "<client_secret>",
    "scopes": ["public_profile"],
    "auth_url": "https://www.facebook.com/v5.0/dialog/oauth",
    "token_url": "https://graph.facebook.com/oauth/access_token",
    "redirect_url": f"http://localhost:{PORT}/facebook-callback",
}
```  