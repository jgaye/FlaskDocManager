import pathlib

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
  return "<h1>" + document + " downloaded</h1>"

def delete(document):
  fullPath = pathlib.Path(testDirectory + document)
  fullPath.unlink()
  # TODO check that the deletion was successful
  # TODO give the user a log message to confirm the delete was successful
  return "<h1>" + fullPath.as_uri() + " deleted</h1>"