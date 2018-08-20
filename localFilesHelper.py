import pathlib

testDirectory = pathlib.Path('/Users/Marvin/projects/FlaskDocManager/testFolder')

def list():
  documents = []
  for currentFile in testDirectory.iterdir():  
    document = {}
    document['name'] = currentFile.name
    document['path'] = currentFile.as_uri()
    documents.append(document)
  return documents

def download(document):
  return "<h1>" + document + " downloaded</h1>"

def delete(document):
  return "<h1>" + document + " deleted</h1>"