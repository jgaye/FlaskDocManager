from flask import (Flask, render_template)

# change type here
# list(), download(), delete() and upload() reserved here
from localFilesHelper import *

app = Flask(__name__)

@app.route("/")
def hello():
    return "This is the upload page"

# Listing page
@app.route("/index")
def index():

  # Get the list of documents
  documents = list()

  # Display the list with controls
  return render_template('listPage.html', documents = documents)