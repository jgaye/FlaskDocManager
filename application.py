import os 
from flask import (Flask, flash, request, session, render_template, redirect, url_for)

'''
  application setup
'''
application = Flask(__name__, instance_relative_config=True)
application.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY=b'gH20EwUgZC#E',
    # store the database in the instance folder
    DATABASE=os.path.join(application.instance_path, 'user.sqlite'),
)

# ensure the instance folder exists
try:
    os.makedirs(application.instance_path)
except OSError:
    pass

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

import db
db.init_app(application)

'''
  auth routes
'''

from helpers.auth import auth_login

# Login page
@application.route("/", methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    result = auth_login(request)

    if result is None:
      return redirect(url_for('index'))
    flash(result)

  return render_template('login.html')

'''
  doc management setup and routes
'''

# change storage location here
# list(), download(), delete() and upload() reserved here

# uncomment for local file management
# from localFilesHelper import list, download, delete, upload

# uncomment for S3 file management
# from S3Helper import list, download, delete, upload

# Listing page
@application.route("/index")
def index():

  # Get the list of documents
  documents = list()

  # Display the list with controls
  return render_template('listPage.html', documents = documents)

@application.route("/<string:document>", methods=['GET', 'POST'])
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

@application.route('/upload', methods=['GET', 'POST'])
def upload_document():
  if request.method == 'POST':
    # Try to perform the upload and get a confirmation message
    result = upload(request)

    # Flash allows to show the confirmation message at index
    flash(result)
    return redirect(url_for('index'))

  return render_template('uploadPage.html')
