import os
from flask import (Flask, flash, request, render_template, redirect, url_for)
from werkzeug.utils import secure_filename

# change type here
# list(), download(), delete() and upload() reserved here
from localFilesHelper import *

UPLOAD_FOLDER = './testFolder'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'pptx', 'docx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Should I use the Flask-Uploads extension instead ?
@app.route('/upload', methods=['GET', 'POST'])
def upload_document():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('index'))
  return render_template('uploadPage.html')

# Listing page
@app.route("/index")
def index():

  # Get the list of documents
  documents = list()

  # Display the list with controls
  return render_template('listPage.html', documents = documents)

@app.route("/download/<string:document>", methods=['GET'])
def download_document(document):
  result = download(document)
  return redirect(url_for('index'))

@app.route("/delete/<string:document>", methods=['POST'])
def delete_document(document):
  result = delete(document)
  return redirect(url_for('index'))
