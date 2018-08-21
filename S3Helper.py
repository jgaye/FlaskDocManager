import os
import boto3, botocore
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'pptx', 'docx'])

S3_BUCKET                 = os.environ.get("S3_BUCKET_NAME")
S3_KEY                    = os.environ.get("S3_ACCESS_KEY")
S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

def list():
  try:
    # returns only the first 1000 elements of S3
    s3Contents = s3.list_objects(Bucket=S3_BUCKET)['Contents']
  except Exception as e:
    # This is a catch all exception, edit this part to fit your needs.
    return "Listing failed with: " + str(e)

  # Transform the data to use the expected schema
  documents = []
  for currentFile in s3Contents:  
    document = {}
    document['name'] = currentFile['Key']
    documents.append(document)
  return documents

def download(document):
  # Download the file in this directory
  return "not implemented"

def delete(document):
  try:
    s3.delete_object(Bucket=S3_BUCKET, Key=document)
    return document + ' was successfully deleted'
  except Exception as e:
    # This is a catch all exception, edit this part to fit your needs.
    return "Delete failed with: " + str(e)

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
      s3.upload_fileobj(
          file,
          S3_BUCKET,
          filename,
          ExtraArgs={
              "ContentType": file.content_type
          }
      )

      return filename + ' was successfully uploaded'

    except Exception as e:
      # This is a catch all exception, edit this part to fit your needs.
      return "Upload failed with: " + str(e)
