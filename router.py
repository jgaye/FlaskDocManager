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

@app.route("/<string:document>/download", methods=['GET'])
def download_document(document):
  result = download(document)
  return result

@app.route("/<string:document>/delete", methods=['GET'])
def delete_document(document):
  result = delete(document)
  return result
