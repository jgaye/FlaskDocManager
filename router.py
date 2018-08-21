from flask import (Flask, flash, request, render_template, redirect, url_for)

# change type here
# list(), download(), delete() and upload() reserved here
from localFilesHelper import *

app = Flask(__name__)
app.secret_key = b'mySecretKeyForFlash'


# Should I use the Flask-Uploads extension instead ?
@app.route('/upload', methods=['GET', 'POST'])
def upload_document():
  if request.method == 'POST':
    # Try to perform the upload and get a confirmation message
    result = upload(request)

    # Flash allows to show the confirmation message at index
    flash(result)
    return redirect(url_for('index'))

  return render_template('uploadPage.html')

# Listing page
@app.route("/index")
def index():

  # Get the list of documents
  documents = list()

  # Display the list with controls
  return render_template('listPage.html', documents = documents)

@app.route("/<string:document>", methods=['GET', 'POST'])
def act_on_document(document):
  if request.method == 'GET':
    # Try to perform the download and get a confirmation message
    result = download(document)

    # Flash allows to show the confirmation message at index
    flash(result)
    return redirect(url_for('index'))

  # the method should be DELETE but the template doesn't support DELETE
  elif request.method == 'POST':
    # Try to perform the delete and get a confirmation message
    result = delete(document)

    # Flash allows to show the confirmation message at index
    flash(result)
    return redirect(url_for('index'))
