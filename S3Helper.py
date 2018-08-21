import os
import boto3, botocore

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
  # returns only the first 1000 elements of S3
  s3Contents = s3.list_objects(Bucket=S3_BUCKET)['Contents']

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
  return "not implemented"

def upload(request):
  return "not implemented"