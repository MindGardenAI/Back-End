import os
from flask import Flask, request, url_for, redirect
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
oauth = OAuth(app)

# Google OAuth registration
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"), # TODO: get google client ID
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"), # TODO: get google client Secret
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

@app.route("/")
def home():
    return "<h1>Hello MindGardenAI, from Flask</h1>"


@app.route("/blingbling")
def blingbling():
    return "<div>Yahoooooo</div>"



@app.route("/add_entry", methods = ["POST"])
def add_entry():
    request_data = request.get_json()

    id = request_data["id"]
    title = request_data["title"]

    out = f"{id} + {title}"
    return out
    
# User login (OAuth)
@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)

# Route that users get redirected to when authorized
@app.route('/authorize')
def authorize():
    token = oauth.twitter.authorize_access_token()
    resp = oauth.twitter.get('account/verify_credentials.json')
    resp.raise_for_status()
    profile = resp.json()
    # do something with the token and profile
    return redirect('/')
        

@app.route("/<usr>")
def user(usr):
    return usr

if __name__ == "__main__":
    app.run(debug=True)