import os 
from flask import (Flask, flash, session, request, render_template, redirect, url_for, send_from_directory)

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

from helpers.auth import auth_login, auth_logout, auth_register

# Login page
@application.route("/", methods=['GET', 'POST'])
@application.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    result = auth_login(request)

    if result is None:
      return redirect(url_for('index'))
    flash(result)

  return render_template('login.html')

@application.route("/logout")
def logout():
  result = auth_logout()

  flash(result)

  return redirect(url_for('login'))

@application.route("/register", methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    result = auth_register(request)

    if result is None:
      flash("User successfully registered. Now please login")
      return redirect(url_for('login'))

    flash(result)
    return redirect(url_for('register'))

  return render_template('register.html')

'''
  doc management setup and routes
'''

# change storage location here
# list(), download(), delete() and upload() reserved here

# uncomment for local file management
# from localFilesHelper import list, download, delete, upload

# uncomment for S3 file management
from helpers.S3Helper import list, download, delete, upload, share, unshare

# Listing page
@application.route("/index")
def index():

  # Get the list of documents this user owns
  privateDocuments = list('home/' + session['username'])

  # Get the list of publicly shared documents
  publicDocuments = list('home/public')

  # If we have a string it is an error message  
  if type(privateDocuments) is str: 
    flash(privateDocuments)
    privateDocuments = []
  if type(publicDocuments) is str: 
    flash(publicDocuments)
    publicDocuments = []

  # Display the list with controls
  return render_template('listPage.html', privateDocuments = privateDocuments, publicDocuments = publicDocuments)

@application.route("/<string:document>", methods=['GET', 'POST'])
def act_on_document(document):
  if request.method == 'GET':
    # Try to perform the download and get 
    # the folder in which it was downloaded
    # the filename
    result = download(document)

    # if result is a string, then it's an error message
    if type(result) is str:  
      flash(result)
      return redirect(url_for('index'))

    # TODO actually check that the result has the correct shape
    return send_from_directory(result[0], result[1], as_attachment=True)

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

@application.route('/share/<string:document>', methods=['POST'])
def share_document(document):
  # Share the document from private to public folder
  result = share(document)

  flash(result)
  return redirect(url_for('index'))

@application.route('/unshare/<string:document>', methods=['POST'])
def unshare_document(document):
  # Share the document from private to public folder
  result = unshare(document)

  flash(result)
  return redirect(url_for('index'))

