# Flask Document Manager

A simple Document Manager with user access built with Flask and python3.  
All files are stored and managed in an Amazon S3 bucket, accessed with the boto3 SDK. Access rights to the files are managed through Amazon IAM policies.  
The application users are managed from an SQLite3 DB.  

In this Flask application you can:
- Register users with a username, password, and S3 user credentials.
- Login / Logout of the Document Manager.
- See the list of documents you own in the S3 bucket. You can download and delete each one of them.
- See the list of documents publicly available to all users in the S3 bucket. You can download and delete each one of them.
- 'Share' a file you own, which makes it public; and 'Unshare' a public file, which makes it visible only to your user.
- Upload documents to your private list of documents. The documents file extensions are limited to 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'pptx' or 'docx'.

## Quickstart

To setup the App:

Open your terminal at the location of the app.

> export FLASK_APP=application.py  
> flask init-db  
> flask run  

Then browse to localhost:5000

## Setup S3

### Create a bucket architecture

### Create the file access policy

### Create group and users