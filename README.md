# Flask Document Manager

A simple Document Manager with user access built with Flask and python3.  
All files are stored and managed in an Amazon S3 bucket, accessed with the boto3 SDK. Access rights to the files are managed through Amazon IAM policies.  
The local users are managed with an SQLite3 DB.  

In this Flask application you can:
- Register users with a username, password, and S3 user credentials.
- Login / Logout of the Document Manager.
- See the list of documents you own in the S3 bucket. You can download and delete each one of them.
- See the list of documents publicly available to all users in the S3 bucket. You can download and delete each one of them.
- 'Share' a file you own, which makes it public; and 'Unshare' a public file, which makes it visible only to your user.
- Upload documents to your private list of documents. The documents file extensions are limited to 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'pptx' or 'docx'.

## Quickstart

You need to have Python3 and virtualenv installed on your machine.
The app uses Flask 1.0.2 , Python 3.6.5 (should come with Flask), boto3 1.7.81 and botocore 1.10.81. Those are packaged in the included virtual environment.

Open your terminal at the location of the app, then run the following commands:
> source virt/bin/activate
> export FLASK_APP=application.py  
> export FLASK_ENV=development  
> flask init-db  
> flask run  

Browse to localhost:5000

To use the App, you will have to setup a S3 bucket, users and policies (see next section).

Once that's done, register your user in the app:
- the selected username must be the same as the Amazon username, to the case.
- use any password you want.
- use the name S3 bucket you created, found in S3, for the S3 Bucket entry .
- use your Amazon user Access key ID for the S3 Key entry, and your Amazon user Secret access key for the S3 Secret entry. You will find both in the Security credentials tabs of your user in IAM. You might have to generate new keys.

If you messed something up and need to reset the user database of the app, open your terminal at the location of the app and do:
> flask init-db

## Setup S3

### Create the bucket architecture

The application expects a specific S3 bucket architectue to handle private and public folder for users.  
To set it up, go to Amazon S3 web console.
1. Create a bucket, it can have any name you want. Default bucket options are ok.
2. In the root of that bucket, create a folder named `home`.
3. In the `home/` folder, create a folder named `public`. It will hold all files that are available to all users.
4. In that same `home/` folder, create one folder for each of your expected Amazon users. Those folder must have the exact same name as the user's username (the users will be created in one of the net sections). Each folder will hold files that are private to the corresponding user.

### Create the file access policy

The file access policy will allow all users to see and managed files in the `home/public/` folder, and to have access to their own private folder `home/{username}`.  
We are going to set the policy up and apply it to a whole group.
1. Go to the IAM management console, to the Policies tab and `Create policy`.  
2. In the JSON editor of the policy, paste the code you''ll find just below. See [this blog post](https://aws.amazon.com/blogs/security/writing-iam-policies-grant-access-to-user-specific-folders-in-an-amazon-s3-bucket/) and [this comment](https://forums.aws.amazon.com/thread.jspa?threadID=277445&tstart=0) for more information on how that policy works.  
3. Review and name the policy with a name of your choosing.  
4. Go back to the IAM management console, and create a new group. Use any name you want.  
5. In the Permissions tab of the group, attach the previously created policy.  
We now have a group that abide by our file access policy

Policy code:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowUserToSeeBucketListInTheConsole",
            "Action": [
                "s3:ListAllMyBuckets",
                "s3:GetBucketLocation"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::*"
            ]
        },
        {
            "Sid": "AllowRootAndHomeListingOfCompanyBucket",
            "Action": [
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::flask-doc-manager-documents"
            ],
            "Condition": {
                "StringEqualsIfExists": {
                    "s3:prefix": [
                        "",
                        "home/"
                    ],
                    "s3:delimiter": [
                        "/"
                    ]
                }
            }
        },
        {
            "Sid": "AllowListingOfUserFolder",
            "Action": [
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::flask-doc-manager-documents"
            ],
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "home/${aws:username}/*",
                        "home/${aws:username}",
                        "home/public/*",
                        "home/public"
                    ]
                }
            }
        },
        {
            "Sid": "AllowAllS3ActionsInUserFolder",
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::flask-doc-manager-documents/home/${aws:username}/*",
                "arn:aws:s3:::flask-doc-manager-documents/home/public/*"
            ]
        }
    ]
}
```

### Create users

The final step consists in creating our S3 users, link them to the group and get their Amazon credentials.
1. In the IAM management console, go to the Users tab. Add a new user.
2. Give the user the name that corresponds to one of the folders created in the 'home/' folder of the bucket. Do not use the name `public`.
3. Tick the `Programmatic access` Access type. Click Next.
4. In the Add user to group section, select the group you created in the previous step. Click Next.
5. Review and create the user.
6. You can grab the `Access key ID` and `Secret access key` in the next screen to be used in the Flask Doc Manager app register screen.

Repeat the above steps for each user you want to create.


You can now register your users in the Flask Doc Management app, and manage the files stored in their S3 folder, and in the `public` folder.


