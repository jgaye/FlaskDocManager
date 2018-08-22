A simple Document Manager built with Flask and Python3.
User DB is the integrated SQLite3 of Python3.
Documents stored in Amazon S3 buckets.

- Register users with a username, password, and S3 user credentials.
- Login / Logout of the Document Manager.
- Index page: see the list of your S3 files. You can download and delete each one of them.
- Upload page: upload one file to your S3. Limited to 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'pptx', 'docx' extensions.

To setup the App:

Open your terminal at the location of the app.

> export FLASK_APP=application.py
> flask init-db
> flask run  

Then browse to localhost:5000