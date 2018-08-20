from flask import Flask
from localFilesHelper import *

app = Flask(__name__)

@app.route("/")
def hello():
    return "This is the upload page"

@app.route("/index")
def index():
  return list()