from flask import Flask, redirect, request, session

import requests

app = Flask(__name__)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

PORT = 1338

# GitHub OAuth2 configuration

github_oauth_config = {
    "client_id": "<client_id>",
    "client_secret": "<client_secret>",
    "scopes": ["user:email"],
    "auth_url": "https://github.com/login/oauth/authorize",
    "token_url": "https://github.com/login/oauth/access_token",
    "redirect_url": f"http://localhost:{PORT}/github-callback",
}

# Facebook OAuth2 configuration
# https://developers.facebook.com/apps/
facebook_oauth_config = {
    # MyCoolApp
    "client_id": "<client_id>",
    "client_secret": "<client_secret>",
    "scopes": ["public_profile"],
    "auth_url": "https://www.facebook.com/v5.0/dialog/oauth",
    "token_url": "https://graph.facebook.com/oauth/access_token",
    "redirect_url": f"http://localhost:{PORT}/facebook-callback",
}

oauth_state_string = "randomstring"
logged_in_as_user = "Github"

@app.route("/")
# def main():
#     return """
#         <h2>Login with GitHub</h2>
#         <a href="/github-login">Login with GitHub</a>
#         <h2>Login with Facebook</h2>
#         <a href="/facebook-login">Login with Facebook</a>
#     """
def main():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>OAuth Demo</title>
  <!-- Bootstrap CSS -->
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"
  />
</head>
<body class="bg-light">
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <a class="navbar-brand" href="#">OAuth Demo</a>
    </div>
  </nav>

  <!-- Main container -->
  <div class="container mt-5">
    <h1 class="mb-4">Welcome to MyCoolApp!</h1>
    <div class="row g-3">
      <!-- GitHub Card -->
      <div class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="card-title">GitHub</h5>
            <p class="card-text">Login with your GitHub account</p>
            <a href="/github-login" class="btn btn-primary">Login with GitHub</a>
          </div>
        </div>
      </div>
      <!-- Facebook Card -->
      <div class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="card-title">Facebook</h5>
            <p class="card-text">Login with your Facebook account</p>
            <a href="/facebook-login" class="btn btn-primary">Login with Facebook</a>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>

  <!-- Bootstrap JS (optional, for interactive components) -->
  <script
    src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js">
  </script>
</body>
</html>
    """
@app.route("/github-login")
def github_login():
    return redirect(build_auth_url(github_oauth_config))

@app.route("/facebook-login")
def facebook_login():
    return redirect(build_auth_url(facebook_oauth_config))

@app.route("/github-callback")
def github_callback():
    return handle_oauth_callback(github_oauth_config)

@app.route("/facebook-callback")
def facebook_callback():
    global logged_in_as_user
    logged_in_as_user = "Facebook"
    return handle_oauth_callback(facebook_oauth_config)

@app.route("/success")
def success():
    return "Success! You are logged in."

def build_auth_url(oauth_config):
    params = {
        "client_id": oauth_config["client_id"],
        "redirect_uri": oauth_config["redirect_url"],
        "scope": ",".join(oauth_config["scopes"]),
        "state": oauth_state_string,
    }
    return f"{oauth_config['auth_url']}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

def handle_oauth_callback(oauth_config):
    state = request.args.get("state")
    if state != oauth_state_string:
        return "Invalid OAuth state", 400

    code = request.args.get("code")
    print("Code: ", code)
    data = {
        "client_id": oauth_config["client_id"],
        "client_secret": oauth_config["client_secret"],
        "code": code,
        "redirect_uri": oauth_config["redirect_url"],
    }
    response = requests.post(oauth_config["token_url"], data=data)
    if response.status_code != 200:
        return f"Failed to exchange code for access token: {response.text}", response.status_code

    '''
    The result of the response type when using GitHub:
    response.text
    'access_token=<access_token>&scope=user%3Aemail&token_type=bearer'

    And this when using facebook:
    response.text
    '{"access_token":"EAAVf00o...","token_type":"bearer","expires_in":5111569}'
    '''

    content_type = response.headers.get("content-type")
    if 'application/json' in content_type:
        token_response = response.json()
        token = token_response.get("access_token")
        print("Access Token: ", token)
        if logged_in_as_user == "Facebook":
            return get_facebook_user_info(oauth_config, token)
        else:
            return get_github_user_info(token)
    else:
        # Parse response text for GitHub
        token = response.text.split('=')[1].split('&')[0]
        print("Access Token: ", token)
        return get_github_user_info(token)

def get_facebook_user_info(oauth_config, token):
    params = {"fields": "name"}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://graph.facebook.com/v13.0/me", params=params, headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        return f"Welcome, {user_info['name']}!"
    else:
        return f"Failed to get user information from Facebook: {response.text}", response.status_code

def get_github_user_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        return f"Logged in as Github user: {user_info['login']}"
    else:
        return f"Failed to get user information from GitHub: {response.text}", response.status_code


# C:\Users\<username>\AppData\Local\Programs\Python\Python312\python.exe: can't open file 'C:\\Program': [Errno 2] No such file or directory
# https://stackoverflow.com/a/44668958/3670782
# https://intellij-support.jetbrains.com/hc/en-us/community/posts/11602067518226-C-Program-Files-Python311-python-exe-can-t-open-file-C-Program-Errno-2-No-such-file-or-directory
# To solve it, change the "debug" to False when debugging.

if __name__ == "__main__":
    app.run(port=PORT, debug=False)
