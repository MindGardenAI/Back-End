import json

from flask import Flask, request, url_for, redirect, render_template, session, url_for, jsonify
from authlib.integrations.flask_client import OAuth
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from openaihelper import OpenAiHelper
from dbhelper import dbhelper


assistant = OpenAiHelper()
helper = dbhelper()


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)


@app.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4)
)

# Auth0 Code that i copied from the documentation
@app.route("/login")
def login():
    print(url_for("callback", _external=True))
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )
    
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )



@app.route("/add_entry", methods = ["POST"])
def add_entry():
    
    
    request_data = request.get_json()

    title = request_data["title"]
    body = request_data["body"]
    
    out = helper.add_entry(title, body)
    return str(out)

@app.route("/get_user_entries", methods = ["POST"])
def get_user_entries():
    request_data = request.get_json()
    
    user = request_data["uid"]
    
    entries = helper.get_user_entries(user)

    return entries

@app.route("/get_user_entries", methods = ["POST"])
def get_user_entries():
    request_data = request.get_json()
    
    user = request_data["uid"]
    
    entries = helper.get_todays_entries(user)

    return entries

@app.route("/<usr>")
def user(usr):
    return usr

@app.route("/singleaffirmation")
def singleaffirmation():
    return assistant.makeRandomAffirmation()

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")

