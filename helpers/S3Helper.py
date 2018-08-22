import os
import boto3, botocore
from flask import session
from werkzeug.utils import secure_filename
from urllib.parse import quote

DOWNLOAD_FOLDER = './downloadFolder/'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'pptx', 'docx'])

def open_s3_session(s3_key, s3_secret):

  return boto3.client(
    "s3",
    aws_access_key_id=s3_key,
    aws_secret_access_key=s3_secret
  )

def list(prefix):
  try:
    # open the session
    s3 = open_s3_session(session['s3_key'], session['s3_secret'])

    # returns only the first 1000 elements of S3
    s3Contents = s3.list_objects(Bucket=session['s3_bucket'], Prefix=prefix)['Contents']
    # s3Contents = s3.buckets.all()
  except Exception as e:
    return "Listing failed with: " + str(e)
  finally:
    # the session cannot be closed, but can be forgotten
    del s3

  # Transform the data to use the expected schema
  documents = []
  for currentFile in s3Contents:  
    document = {}

    # dirty split of the Key to get only the files, and only the names
    filename = currentFile['Key'].split('/')[-1]

    if filename:
      document['name'] = quote(filename)
      documents.append(document)
  return documents

def download(document):
  # downloads to the local DOWNLOAD_FOLDER, will that work on AWS?
  try:
    s3 = open_s3_session(session['s3_key'], session['s3_secret'])

    s3.download_file(session['s3_bucket'], 'home/' + session['username'] + '/' + document, DOWNLOAD_FOLDER + document)  
    return document + ' was successfully downloaded'
  except Exception as e:
    return "Download failed with: " + str(e)
  finally:
    del s3

def delete(document):
  try:
    s3 = open_s3_session(session['s3_key'], session['s3_secret'])

    s3.delete_object(Bucket=session['s3_bucket'], Key='home/' + session['username'] + '/' + document)
    return document + ' was successfully deleted'
  except Exception as e:
    return "Delete failed with: " + str(e)
  finally:
    del s3

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

    # try to upload to S3
    try:
      s3 = open_s3_session(session['s3_key'], session['s3_secret'])

      # upload to the current user folder in S3
      UPLOAD_FOLDER = 'home/' + session['username'] + '/'

      s3.upload_fileobj(
          file,
          session['s3_bucket'],
          UPLOAD_FOLDER + filename,
          ExtraArgs={
              "ContentType": file.content_type
          }
      )

      return filename + ' was successfully uploaded'

    except Exception as e:
      return "Upload failed with: " + str(e)
    finally:
      del s3
