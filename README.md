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

You need to have Flask 1.0.2 , Python 3.6.5 (should come with Flask), boto3 1.7.81 and botocore 1.10.81.

Open your terminal at the location of the app.

> export FLASK_APP=application.py  
> export FLASK_ENV=development  
> flask init-db  
> flask run  

Browse to localhost:5000

To use the App, you will have to setup a S3 bucket, users and policies (see next section).

Once that's done, register your user in the app:
- the selected username must be the same as the Amazon username, to the case.
- use any password you want.
- use the name S3 bucket you setup, found in S3, for the S3 Bucket entry .
- use your Amazon user Access key ID for the S3 Key entry, and your Amazon user Secret access key for the S3 Secret entry. You will find both in the Security credentials tabs of your user in IAM. You might have to generate new keys.

If you messed something up and need to reset the use database of the app, open your terminal at the location of the app and do:
> flask init-db

## Setup S3

### Create a bucket architecture

### Create the file access policy

### Create group and users