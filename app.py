import json
from bson import ObjectId
from flask import Flask, request, url_for, redirect, render_template, session, url_for, jsonify, Response
from flask_cors import CORS, cross_origin
from authlib.integrations.flask_client import OAuth
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from openaihelper import OpenAiHelper
from dbhelper import dbhelper

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

assistant = OpenAiHelper()
helper = dbhelper()


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

allowed_domains = ["https://mindgardenai.tech:443",
                   "http://localhost:3000",
                   "http://localhost:8080",
                   "https://back-end-qukwylxm3a-uk.a.run.app:443",
                   "cluster0-shard-00-01.vk4vz.mongodb.net:27017",
                   "cluster0-shard-00-00.vk4vz.mongodb.net:27017"]

cors = CORS(app, origins=allowed_domains)
# app.config['CORS_HEADERS'] = 'Content-Type'

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



@app.route("/add_entry", methods=["GET", "POST"])
def add_entry():
    
    
    request_data = request.get_json()

    user_id = request_data["uid"]
    body = request_data["body"]
    
    out = helper.add_entry(user_id, body)
    return str(out)

@app.route("/get_user_entries", methods=["GET", "POST"])
def get_user_entries():
    request_data = request.get_json()
    
    user = request_data["uid"]
    
    entries = helper.get_user_entries(str(user))

    print(type(entries))
    print(entries)
    return json.dumps(entries, default=str)

@app.route("/get_todays_entries", methods=["GET", "POST"])
def get_todays_entries():
    request_data = request.get_json()
    
    user = request_data["uid"]
    
    entries = helper.get_todays_entries(str(user))

    return json.dumps(entries, default=str)

@app.route("/add_goal", methods=["GET", "POST"])
def add_goal():
    request_data = request.get_json()
    user = request_data["uid"]
    description = request_data["description"]
    complete_by_date = request_data["complete_by_date"]
    
    out =  helper.add_goal(user, description, complete_by_date)
    
    return str(out)

@app.route("/get_user_goals", methods=["GET", "POST"])
def get_user_goals():
    request_data = request.get_json()
    user = request_data["uid"]
    goals = helper.get_user_goals(str(user))
    return json.dumps(goals, default=str)
    
@app.route("/singleaffirmation")
def singleaffirmation():
    return assistant.makeRandomAffirmation()

@app.route("/guidedaffirmation", methods = ["POST"])
def guidedaffirmation():
    data = request.json
    problem = data.get('problem')
    affirmations = assistant.makeGuidedAffirmation(problem)
    print(problem)
    print(affirmations)
    return affirmations

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")



