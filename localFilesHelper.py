import pathlib
import urllib.request

testDirectory = '/Users/Marvin/projects/FlaskDocManager/testFolder/'

def list():
  documents = []
  for currentFile in pathlib.Path(testDirectory).iterdir():  
    document = {}
    document['name'] = currentFile.name
    document['path'] = currentFile.as_uri()
    documents.append(document)
  return documents

def download(document):
  # Download the file in this directory
  fullPath = pathlib.Path(testDirectory + document)
  urllib.request.urlretrieve(fullPath.as_uri(), document)
  # TODO ask the user where he wants to download the file
  # TODO check that the download was successful
  # TODO display a confirmation message to the user

  return document + " was successfully downloaded"

def delete(document):

  fullPath = pathlib.Path(testDirectory + document)
  fullPath.unlink()

  # TODO check that the deletion was successful
  # TODO give the user a log message to confirm the delete was successful
  return fullPath.as_uri() + " was successfully deleted"