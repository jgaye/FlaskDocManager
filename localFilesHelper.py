import os
import pathlib
import urllib.request
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/Users/Marvin/projects/FlaskDocManager/testFolder/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'pptx', 'docx'])

def list():
  documents = []
  for currentFile in pathlib.Path(UPLOAD_FOLDER).iterdir():  
    document = {}
    document['name'] = currentFile.name
    document['path'] = currentFile.as_uri()
    documents.append(document)
  return documents

def download(document):
  # Download the file in this directory
  fullPath = pathlib.Path(UPLOAD_FOLDER + document)
  urllib.request.urlretrieve(fullPath.as_uri(), document)
  # TODO ask the user where he wants to download the file
  # TODO check that the download was successful
  # TODO display a confirmation message to the user

  return document + " was successfully downloaded"

def delete(document):

  fullPath = pathlib.Path(UPLOAD_FOLDER + document)
  fullPath.unlink()

  # TODO check that the deletion was successful
  # TODO give the user a log message to confirm the delete was successful
  return fullPath.as_uri() + " was successfully deleted"

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload(request):
  # check if the post request has the file part
  if 'file' not in request.files:
    return "No file part"
  file = request.files['file']
  # if user does not select file, browser also
  # submit an empty part without filename
  if file.filename == '':
    return "No selected file"
  if not allowed_file(file.filename):
    return "File extension not allowed for upload"
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return filename + ' was successfully uploaded'