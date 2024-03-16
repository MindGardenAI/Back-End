from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello World, from Flask</h1>"

@app.route("/login")
def login():
    return "<h1>Login here</h1>"

@app.route("/blingbling")
def blingbling():
    return "<div>Yahoooooo</div>"

if __name__ == "__main__":
    app.run(debug=True)