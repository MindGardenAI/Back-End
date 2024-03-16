from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello MindGardenAI, from Flask</h1>"

@app.route("/login")
def login():
    return "<h1>Login here</h1>"

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
    
        

@app.route("/<usr>")
def user(usr):
    return usr

if __name__ == "__main__":
    app.run(debug=True)