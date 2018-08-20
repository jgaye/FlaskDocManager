import pathlib

testDirectory = pathlib.Path('./testFolder')
a = "this is a var"

def list():
  documents = []
  for currentFile in testDirectory.iterdir():  
    documents.append(currentFile.name)
  return "<br>".join(documents)
