from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "This is the upload page"

@app.route("/list")
def fct():
    return "This is the listing page"